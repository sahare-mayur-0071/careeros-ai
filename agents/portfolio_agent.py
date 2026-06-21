from agents.base_agent import BaseAgent
import json

class PortfolioBuilderAgent(BaseAgent):
    def __init__(self):
        super().__init__("Portfolio Builder Agent", "Suggests portfolio projects and GitHub improvements.")

    def build(self, target_role: str, missing_skills: list) -> dict:
        prompt = f"""
        You are a Portfolio Builder Agent. Suggest portfolio projects for a {target_role} to help them practice these missing skills: {', '.join(missing_skills)}.
        Return a JSON object with:
        - project_ideas (list of dicts: title, description, architecture (brief 1 sentence), tech_stack (list of strings))
        - github_improvements (list of strings: tips to make their GitHub stand out)
        """
        return self._call_llm(prompt)
