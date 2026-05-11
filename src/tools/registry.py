from typing import Callable, Dict
from src.tools.generate_theory import generate_theory
from src.tools.search_courses import search_courses
from src.tools.search_youtube import search_youtube

class ToolRegistry:
    """
    A Hash Map to store our tools in O(1) lookup time.
    """
    def __init__(self):
        self._tools: Dict[str, Callable] = {}

    def register_tool(self, name: str, func: Callable):
        self._tools[name] = func

    def get_tool(self, name: str) -> Callable:
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' not found in registry.")
        return self._tools[name]

    def list_tools(self) -> list:
        return list(self._tools.keys())

tool_registry = ToolRegistry()
tool_registry.register_tool("generate_theory", generate_theory)
tool_registry.register_tool("search_courses", search_courses)
tool_registry.register_tool("search_youtube", search_youtube)
