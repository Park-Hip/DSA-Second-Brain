from collections import deque
from src.dsa.graph import TaskGraph
from src.dsa.node import TaskStatus
from src.tools.registry import ToolRegistry
from src.memory.cache import MemoryCache

class ExecutorAgent:
    """
    Pulls the topological sort from the DAG and executes tasks in order using tools.
    """
    def __init__(self, registry: ToolRegistry, cache: MemoryCache):
        self.registry = registry
        self.cache = cache

    def execute_graph_generator(self, graph: TaskGraph):
        """
        Yields status updates as it processes the Queue.
        """
        try:
            execution_order = graph.topological_sort()
            queue = deque(execution_order)
            
            while queue:
                task_id = queue.popleft()
                node = graph.get_node(task_id)
                
                if not node:
                    continue
                
                yield {"task_id": task_id, "name": node.name, "status": "PROCESSING"}
                node.status = TaskStatus.IN_PROGRESS
                
                if self.cache.has(task_id):
                    node.status = TaskStatus.COMPLETED
                    yield {"task_id": task_id, "name": node.name, "status": "CACHED"}
                    continue
                    
                try:
                    theory_tool = self.registry.get_tool("generate_theory")
                    course_tool = self.registry.get_tool("search_courses")
                    youtube_tool = self.registry.get_tool("search_youtube")
                    
                    theory_result = theory_tool(node.name)
                    course_result = course_tool(node.name)
                    youtube_result = youtube_tool(node.name)

                    result = {
                        "theory": theory_result,
                        "courses": course_result,
                        "youtube": youtube_result
                    }
                    
                    self.cache.save(task_id, result)
                    node.status = TaskStatus.COMPLETED
                    yield {"task_id": task_id, "name": node.name, "status": "COMPLETED"}
                except Exception:
                    node.status = TaskStatus.FAILED
                    yield {"task_id": task_id, "name": node.name, "status": "FAILED"}

        except ValueError as e:
            yield {"error": str(e), "status": "ABORTED"}
