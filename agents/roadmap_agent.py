from agents.base_agent import BaseAgent
import json

class LearningRoadmapAgent(BaseAgent):
    def __init__(self):
        super().__init__("Learning Roadmap Agent", "Generates 30/60/90 day learning plans.")

    def generate(self, missing_skills: list, target_role: str) -> dict:
        prompt = f"""
        You are a Learning Roadmap Agent. Create a roadmap to learn these missing skills: {', '.join(missing_skills)} for a {target_role}.
        Return a JSON object with:
        - roadmap_30_days (dict: focus, weekly_goals (list of strings), resources (list of strings))
        - roadmap_60_days (dict: focus, weekly_goals, resources)
        - roadmap_90_days (dict: focus, weekly_goals, resources)

        Make resources specific (e.g. "FreeCodeCamp course X", "Book Y").
        """
        return self._call_llm(prompt)
