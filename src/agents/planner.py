from src.dsa.graph import TaskGraph
from src.dsa.node import TaskNode
from src.agents.llm_client import LLMClient
from src.core.logger import logger
from src.core.configs import settings

class PlannerAgent:
    """
    Use LLM to decompose a complicated subject into sub concepts and construct a 
    Directed Acyclic Graph (DAG)
    """

    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def plan_subject(self, subject: str) -> TaskGraph:
        """
        Construct DAG
        """
        user_prompt_template = settings.prompts_yaml.get("planner", {}).get("user_prompt", "Break down: {subject}")
        user_prompt = user_prompt_template.format(subject=subject)
        
        system_prompt = settings.prompts_yaml.get("planner", {}).get("system_prompt", "PLANNER_PROMPT_NOT_FOUND")
        
        parsed_data = self.llm.generate_json(system_prompt, user_prompt)
        
        graph = TaskGraph()
        
        for task_dict in parsed_data.get("tasks", []):
            node = TaskNode(
                task_id=task_dict["id"],
                name=task_dict["name"],
                description=task_dict.get("desc", "")
            )
            graph.add_node(node)
            
        for edge_dict in parsed_data.get("edges", []):
            try:
                graph.add_edge(edge_dict["from"], edge_dict["to"])
            except ValueError as e:
                logger.warning("Skipping invalid edge", error=str(e))
                
        return graph
