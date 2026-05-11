import json
import os
from src.core.logger import logger
from src.dsa.graph import TaskGraph
from src.memory.cache import MemoryCache

DB_DIR = "db"
GRAPH_FILE = os.path.join(DB_DIR, "graph.json")
CACHE_FILE = os.path.join(DB_DIR, "cache.json")

def _ensure_db_dir():
    "Create db folder when it is not existed"
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)

def save_state(graph: TaskGraph, cache: MemoryCache):
    """Save the graph and cache to JSON files."""
    _ensure_db_dir()
    
    try:
        with open(GRAPH_FILE, "w", encoding="utf-8") as f:
            json.dump(graph.to_dict(), f, indent=2)
        
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache.to_dict(), f, indent=2)
            
        logger.info("Successfully serialized state to JSON DB")
    except Exception as e:
        logger.error("Failed to save state to DB", error=str(e))

def load_state() -> tuple[TaskGraph, MemoryCache]:
    """Loads the  graph and cache from JSON files."""
    _ensure_db_dir()
    
    graph = TaskGraph()
    cache = MemoryCache()
    
    try:
        if os.path.exists(GRAPH_FILE):
            with open(GRAPH_FILE, "r", encoding="utf-8") as f:
                graph_data = json.load(f)
                graph = TaskGraph.from_dict(graph_data)
                
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
                cache = MemoryCache.from_dict(cache_data)
                
        logger.info("Successfully loaded state from JSON DB")
    except Exception as e:
        logger.error("Failed to load state from DB", error=str(e))
        
    return graph, cache
