import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config

from src.agents.llm_client import LLMClient
from src.agents.planner import PlannerAgent
from src.agents.executor import ExecutorAgent
from src.tools.registry import tool_registry
from src.memory.storage import load_state, save_state

def display_lesson_resources(data):
    """Refactored helper to display theory and links from cache."""
    with st.expander("**Lessons & Resources**", expanded=True):
        if isinstance(data, dict):
            st.markdown(data.get("theory", ""))
            st.divider()
            st.markdown("### Study Links")
            
            courses = data.get("courses", [])
            videos = data.get("youtube", [])
                    
            if courses:
                st.markdown("#### Recommended Courses")
                for c in courses:
                    st.markdown(f"* {c}")
                    
            if videos:
                st.markdown("#### YouTube Tutorials")
                for v in videos:
                    st.markdown(f"* {v}")
        else:
            st.info(data)


st.set_page_config(page_title="Second Brain", layout="wide")

if "global_graph" not in st.session_state:
    loaded_graph, loaded_cache = load_state()
    st.session_state.global_graph = loaded_graph
    st.session_state.cache = loaded_cache
if "graph" not in st.session_state:
    st.session_state.graph = None


st.markdown("<h1 style='text-align: center; font-size: 60px;'>🧠 Second Brain</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 24px; color: #888888;'>Breaking complex subjects into simple roadmaps and build your Second Brain via DAG (Directed Acyclic Graph) </p>", unsafe_allow_html=True)
st.markdown("---")

col1, col2, col3 = st.columns([4, 2, 2])
with col1:
    subject = st.text_input("Enter a topic you want to master:", "Machine Learning")
with col2:
    st.write("") 
    st.write("")
    if st.button("Generate Roadmap", use_container_width=True):
        with st.spinner("LLM is decomposing the subject..."):
            client = LLMClient()
            planner = PlannerAgent(client)
            try:
                st.session_state.graph = planner.plan_subject(subject)
                
                st.session_state.global_graph.merge(st.session_state.graph)
                save_state(st.session_state.global_graph, st.session_state.cache)
                
                st.success("Graph Generated and Saved to Second Brain!")
            except Exception as e:
                st.error(f"Error generating graph: {e}")
with col3:
    st.write("")
    st.write("")
    if st.button("Execute Queue", use_container_width=True):
        if st.session_state.graph:
            executor = ExecutorAgent(tool_registry, st.session_state.cache)
            
            status_placeholder = st.empty()
            
            for update in executor.execute_graph_generator(st.session_state.graph):
                if update["status"] == "PROCESSING":
                    status_placeholder.info(f"**Executing:** Generating contents for `{update['name']}`...")
                elif update["status"] == "CACHED":
                    status_placeholder.success(f"**Cache Hit:** Skipping `{update['name']}` (Already in Memory!)")
                elif update["status"] == "COMPLETED":
                    status_placeholder.success(f"**Completed:** `{update['name']}`")
                elif update["status"] == "FAILED":
                    status_placeholder.error(f" **Failed:** Could not process `{update['name']}`")
                    
            save_state(st.session_state.global_graph, st.session_state.cache)
            status_placeholder.success("**Queue Execution Complete!**")
            
            st.rerun() # force the graph colors to update from red to green
        else:
            st.warning("Generate a path first!")

st.markdown("---")
tab1, tab2 = st.tabs(["Roadmap", "Second Brain"])

with tab1:
    if st.session_state.graph:
        with st.container(border=True):
            st.subheader("Skill Tree")
            nodes = []
            edges = []
            
            for node_id, node in st.session_state.graph.nodes.items():
                is_cached = st.session_state.cache.has(node.id)
                nodes.append(Node(id=node.id, 
                                  label=node.name,
                                  size=25, 
                                  shape="dot",
                                  color="#00FFCC" if is_cached else "#FF4B4B"))
                                  
            for node_id, prereqs in st.session_state.graph.prerequisites.items():
                for p_id in prereqs:
                    edges.append(Edge(source=p_id, 
                                      target=node_id, 
                                      color="#AAAAAA"))

            config = Config(width=1500,
                            height=600,
                            directed=True, 
                            physics=False, 
                            hierarchical=True,
                            layout={
                                "hierarchical": {
                                    "enabled": True,
                                    "direction": "LR",
                                    "sortMethod": "directed",
                                    "levelSeparation": 250,
                                    "nodeSpacing": 100
                                }
                            })
                            
            return_value = agraph(nodes=nodes, 
                                  edges=edges, 
                                  config=config)
                                  
            if return_value:
                st.markdown(f"**Selected Node ID:** `{return_value}`")
                if st.session_state.cache.has(return_value):
                    display_lesson_resources(st.session_state.cache.get(return_value))
                else:
                    st.warning("This node has not been executed yet. Run the 'Execute Queue' button to fetch its data.")
    else:
            st.info("Generate a roadmap to see your graph.")

with tab2:
    if len(st.session_state.global_graph.nodes) > 0:   
        col_brain1, col_brain2 = st.columns([4, 2])
        with col_brain1:
            node_names = ["Select a topic to highlight"] + sorted([node.name for node in st.session_state.global_graph.nodes.values()])
            search_query = st.selectbox("Find a topic:", node_names)
            
            if search_query != "Select a topic to highlight":
                if st.button("Delete Topic", use_container_width=True):
                    node_id_to_delete = None
                    for n_id, n in st.session_state.global_graph.nodes.items():
                        if n.name == search_query:
                            node_id_to_delete = n_id
                            break
                    if node_id_to_delete:
                        st.session_state.global_graph.prune_node_and_prerequisites(node_id_to_delete)
                        save_state(st.session_state.global_graph, st.session_state.cache)
                        st.success(f"Successfully deleted '{search_query}' and its prerequisites from the the second brain!")
                        st.rerun()
            
        with col_brain2:
            st.write("")
            st.write("")
            if st.button("Execute Pending Nodes", use_container_width=True):
                executor = ExecutorAgent(tool_registry, st.session_state.cache)
                status_placeholder_brain = st.empty()
                
                for update in executor.execute_graph_generator(st.session_state.global_graph):
                    if update["status"] == "PROCESSING":
                        status_placeholder_brain.info(f"**Executing:** Generating contents for `{update['name']}`...")
                    elif update["status"] == "COMPLETED":
                        status_placeholder_brain.success(f"**Completed:** `{update['name']}`")
                    elif update["status"] == "FAILED":
                        status_placeholder_brain.error(f"**Failed:** Could not process `{update['name']}`")
                        
                save_state(st.session_state.global_graph, st.session_state.cache)
                status_placeholder_brain.success("**Second Brain Update Complete!**")
                st.rerun()
        
        with st.container(border=True):
            global_nodes = []
            global_edges = []
            
            for node_id, node in st.session_state.global_graph.nodes.items():
                is_cached = st.session_state.cache.has(node.id)
                is_searched = (node.name == search_query)
                
                node_color = "#FFD700" if is_searched else ("#00FFCC" if is_cached else "#FF4B4B")
                node_size = 25 if is_searched else 15
                
                global_nodes.append(Node(id=node.id, 
                                         label=node.name,
                                         size=node_size, 
                                         shape="dot",
                                         color=node_color))
                                  
            for node_id, prereqs in st.session_state.global_graph.prerequisites.items():
                for p_id in prereqs:
                    global_edges.append(Edge(source=p_id, 
                                             target=node_id, 
                                             color="#AAAAAA"))

            global_config = Config(width=1500,
                                   height=800,
                                   directed=True, 
                                   physics=True,
                                   hierarchical=False)
                                   
            # Manually overwrite the physics dictionary to bypass streamlit-agraph's buggy Config.__init__
            global_config.physics = {
                "enabled": True,
                "solver": "repulsion",
                "repulsion": {
                    "nodeDistance": 300,
                    "centralGravity": 0.02,
                    "springLength": 150,
                    "damping": 0.09
                }
            }
                            
            global_return = agraph(nodes=global_nodes, 
                                   edges=global_edges, 
                                   config=global_config)
                                   
            if global_return:
                st.markdown(f"**Selected Node ID:** `{global_return}`")
                if st.session_state.cache.has(global_return):
                    display_lesson_resources(st.session_state.cache.get(global_return))
                else:
                    st.warning("This node has not been executed yet. Pressing 'Execute Peding Nodes' to fetch its data.")
    else:
        st.info("Your second brain is empty. Generate a roadmap first!")
