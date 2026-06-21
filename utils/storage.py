import json
import os
from utils.logger import setup_logger

logger = setup_logger(__name__)

MEMORY_FILE = "data/memory.json"

def load_memory() -> dict:
    """Loads user memory from persistent storage."""
    if not os.path.exists("data"):
        os.makedirs("data")
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading memory: {e}")
            return {}
    return {}

def save_memory(data: dict):
    """Saves user memory to persistent storage."""
    if not os.path.exists("data"):
        os.makedirs("data")
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logger.error(f"Error saving memory: {e}")
