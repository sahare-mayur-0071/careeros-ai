from agents.base_agent import BaseAgent
import json

class CertificationAdvisorAgent(BaseAgent):
    def __init__(self):
        super().__init__("Certification Advisor Agent", "Recommends relevant certifications.")

    def recommend(self, target_role: str, acquired_skills: list, missing_skills: list) -> dict:
        prompt = f"""
        You are a Certification Advisor Agent. Recommend certifications for a {target_role}.
        Acquired skills: {', '.join(acquired_skills)}. Missing skills: {', '.join(missing_skills)}.
        Only recommend from: Google, AWS, Microsoft Azure, Coursera, Kaggle.
        
        Return a JSON object with:
        - recommendations (list of dicts: name, provider, difficulty, url_hint, reason (why they should take it based on missing skills))
        """
        return self._call_llm(prompt)
