from agents.base_agent import BaseAgent
import json

class ATSOptimizationAgent(BaseAgent):
    def __init__(self):
        super().__init__("ATS Optimization Agent", "Calculates ATS score and detects issues.")

    def optimize(self, parsed_resume: dict, target_role: str) -> dict:
        prompt = f"""
        You are an ATS Optimization Agent. Analyze this resume for a {target_role} position.
        Return a JSON object with:
        - ats_score (integer 0-100)
        - missing_keywords (list of strings)
        - formatting_issues (list of strings)
        - recommended_improvements (list of actionable bullet points)

        Parsed Resume:
        {json.dumps(parsed_resume, indent=2)}
        """
        return self._call_llm(prompt)
