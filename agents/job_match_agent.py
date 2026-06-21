from agents.base_agent import BaseAgent
import json

class JobMatchingAgent(BaseAgent):
    def __init__(self):
        super().__init__("Job Matching Agent", "Matches user against job roles.")

    def match(self, parsed_resume: dict) -> dict:
        roles = [
            "Software Engineer", "Full Stack Developer", "Data Analyst", 
            "Data Scientist", "AI Engineer", "Machine Learning Engineer",
            "Cloud Engineer", "DevOps Engineer", "Cybersecurity Analyst", "Product Manager"
        ]
        
        prompt = f"""
        You are a Job Matching Agent. Evaluate the resume against these roles: {', '.join(roles)}.
        Return a JSON object with:
        - top_matches (list of dicts: role, match_percentage (0-100 integer), explanation (1 sentence))
        - recommended_career_paths (list of strings: e.g., 'Junior Data Analyst -> Data Scientist')

        Parsed Resume:
        {json.dumps(parsed_resume, indent=2)}
        """
        return self._call_llm(prompt)
