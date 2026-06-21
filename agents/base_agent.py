from utils.llm import get_llm_response
from utils.logger import setup_logger

class BaseAgent:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.logger = setup_logger(self.__class__.__name__)
        
    def _call_llm(self, prompt: str, expect_json: bool = True):
        self.logger.info(f"{self.name} is working...")
        try:
            return get_llm_response(prompt=prompt, expect_json=expect_json)
        except Exception as e:
            self.logger.error(f"Error in {self.name}: {e}")
            return None
