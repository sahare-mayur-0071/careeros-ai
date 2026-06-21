from agents.base_agent import BaseAgent
import json

class SkillGapAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__("Skill Gap Analysis Agent", "Compares profile with target role to identify missing skills.")

    def analyze(self, parsed_resume: dict, target_role: str) -> dict:
        prompt = f"""
        You are a Skill Gap Analysis Agent. Compare this profile to industry standards for {target_role}.
        Return a JSON object with:
        - acquired_skills (list of strings)
        - missing_skills (list of strings)
        - critical_gaps (list of strings: most important missing skills)
        - learning_recommendations (list of strings: prioritized list of what to learn first)

        Parsed Resume:
        {json.dumps(parsed_resume, indent=2)}
        """
        return self._call_llm(prompt)
