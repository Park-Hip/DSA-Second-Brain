from typing import Dict, List, Optional
from src.dsa.node import TaskNode
from collections import deque

class TaskGraph:
    """
    Core implementation of a Directed Acyclic Graph (DAG) for managing task prerequisites.
    """
    def __init__(self):
        self.nodes: Dict[str, TaskNode] = {}
        self.prerequisites: Dict[str, List[str]] = {}
        self.dependents: Dict[str, List[str]] = {}
    
    def __repr__(self):
        return f"TaskGraph(Nodes={len(self.nodes)})"

    def add_node(self, node: TaskNode) -> None:
        """Adds a node to the graph if it doesn't already exist."""
        if node.id not in self.nodes:
            self.nodes[node.id] = node
            self.prerequisites[node.id] = []
            self.dependents[node.id] = []

    def add_edge(self, prereq_id: str, target_id: str) -> None:
        """
        Adds a directed edge from prereq_id to target_id.
        This means 'prereq_id' must be completed before 'target_id'.
        """
        if prereq_id not in self.nodes or target_id not in self.nodes:
            raise ValueError("Both nodes must exist in the graph before adding an edge.")
            
        if prereq_id not in self.prerequisites[target_id]:
            self.prerequisites[target_id].append(prereq_id)
        
        if target_id not in self.dependents[prereq_id]:
            self.dependents[prereq_id].append(target_id)

    def get_node(self, node_id: str) -> Optional[TaskNode]:
        """Retrieves a node by its ID."""
        return self.nodes.get(node_id)
        
    def detect_cycle(self) -> bool:
        """
        Uses Depth-First Search (DFS) to detect if there is a cycle in the DAG.
        Returns True if a cycle is found, False otherwise.
        """
        visited = set()
        recursion_stack = set()
        
        def dfs(node_id: str) -> bool:
            visited.add(node_id)
            recursion_stack.add(node_id)

            for neighbor_id in self.dependents.get(node_id, []):
                if neighbor_id not in visited:
                    if dfs(neighbor_id):
                        return True
                elif neighbor_id in recursion_stack:
                    return True

            recursion_stack.remove(node_id)
            return False

        for node_id in self.nodes:
            if node_id not in visited:
                if dfs(node_id):
                    return True
                    
        return False
        
    def topological_sort(self) -> List[str]:
        """
        Uses Kahn's Algorithm to sort nodes topologically.
        Returns a list of node IDs in execution order.
        Raises ValueError if a cycle is detected during sorting.
        """
        in_degree = {node_id: 0 for node_id in self.nodes}

        for node_id in self.nodes:
            for neighbor_id in self.dependents.get(node_id, []):
                in_degree[neighbor_id] += 1

        queue = deque([node_id for node_id in self.nodes if in_degree[node_id] == 0])
        
        sorted_order = []
        
        while queue:
            current = queue.popleft()
            sorted_order.append(current)

            for neighbor_id in self.dependents.get(current, []):
                in_degree[neighbor_id] -= 1
                if in_degree[neighbor_id] == 0:
                    queue.append(neighbor_id)

        if len(sorted_order) != len(self.nodes):
            raise ValueError("Graph contains a cycle! Topological sort is not possible.")
            
        return sorted_order

    def merge(self, other_graph: 'TaskGraph') -> None:
        """Merges another graph's nodes and edges into this graph."""
        for node_id, node in other_graph.nodes.items():
            self.add_node(node)
            
        for target_id, prereqs in other_graph.prerequisites.items():
            for prereq_id in prereqs:
                self.add_edge(prereq_id, target_id)

    def _remove_single_node(self, node_id: str) -> None:
        """Remove a node and all its connected edges from the Adjacency Lists."""
        if node_id not in self.nodes:
            return
        
        for p_id in self.prerequisites.get(node_id, []):
            if p_id in self.dependents and node_id in self.dependents[p_id]:
                self.dependents[p_id].remove(node_id)
                
        for d_id in self.dependents.get(node_id, []):
            if d_id in self.prerequisites and node_id in self.prerequisites[d_id]:
                self.prerequisites[d_id].remove(node_id)
                
        del self.nodes[node_id]
        if node_id in self.prerequisites:
            del self.prerequisites[node_id]
        if node_id in self.dependents:
            del self.dependents[node_id]

    def prune_node_and_prerequisites(self, node_id: str) -> None:
        """
        Recursively deletes a node and any of its isolated prerequisites.
        """
        if node_id not in self.nodes:
            return
        
        prereqs = list(self.prerequisites.get(node_id, []))
        
        self._remove_single_node(node_id)
        
        for p_id in prereqs:
            if p_id in self.dependents and len(self.dependents[p_id]) == 0:
                self.prune_node_and_prerequisites(p_id)

    def to_dict(self) -> dict:
        return {
            "nodes": {node_id: node.to_dict() for node_id, node in self.nodes.items()},
            "prerequisites": self.prerequisites,
            "dependents": self.dependents
        }

    @classmethod
    def from_dict(cls, data: dict):
        graph = cls()
        graph.prerequisites = data.get("prerequisites", {})
        graph.dependents = data.get("dependents", {})
        
        for node_id, node_data in data.get("nodes", {}).items():
            graph.nodes[node_id] = TaskNode.from_dict(node_data)
            
        return graph
