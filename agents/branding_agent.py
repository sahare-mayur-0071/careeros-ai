from agents.base_agent import BaseAgent
import json

class PersonalBrandingAgent(BaseAgent):
    def __init__(self):
        super().__init__("Personal Branding Agent", "Generates LinkedIn and GitHub branding content.")

    def brand(self, parsed_resume: dict, target_role: str) -> dict:
        prompt = f"""
        You are a Personal Branding Agent. Based on the resume, generate branding materials for a {target_role}.
        Return a JSON object with:
        - linkedin_headline (string)
        - linkedin_about (string)
        - github_readme_intro (string)
        - portfolio_tagline (string)

        Parsed Resume:
        {json.dumps(parsed_resume, indent=2)}
        """
        return self._call_llm(prompt)
