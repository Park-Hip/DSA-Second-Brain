from typing import Any, Dict
from src.core.logger import logger

class MemoryCache:
    """
    Save the theory and learning resources for concepts, preventing redundant API call.
    """
    def __init__(self):
        self._cache: Dict[str, Any] = {}

    def save(self, task_id: str, result_data: Any) -> None:
        self._cache[task_id] = result_data
        logger.info("Saved to cache", task_id=task_id)

    def get(self, task_id: str) -> Any:
        return self._cache.get(task_id)

    def has(self, task_id: str) -> bool:
        return task_id in self._cache

    def size(self) -> int:
        return len(self._cache)

    def to_dict(self) -> dict:
        return self._cache

    @classmethod
    def from_dict(cls, data: dict):
        cache = cls()
        cache._cache = data
        return cache
