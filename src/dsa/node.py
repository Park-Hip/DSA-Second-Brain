class TaskStatus:
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class TaskNode:
    """
    Represents a single task (or topic) in our learning Directed Acyclic Graph (DAG).
    DSA Concept: Node in a Graph/Tree.
    """
    def __init__(self, task_id: str, name: str, description: str = ""):
        self.id = task_id
        self.name = name
        self.description = description
        self.status = TaskStatus.PENDING

    def __repr__(self):
        return f"TaskNode(id='{self.id}', name='{self.name}', status='{self.status}')"

    def __eq__(self, other):
        if not isinstance(other, TaskNode):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
        
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data: dict):
        node = cls(task_id=data["id"], name=data["name"], description=data.get("description", ""))
        node.status = data.get("status", TaskStatus.PENDING)
        return node
