from agents.base_agent import BaseAgent
import json

class ResumeIntelligenceAgent(BaseAgent):
    def __init__(self):
        super().__init__("Resume Intelligence Agent", "Parses and structures raw resume text.")

    def process(self, resume_text: str) -> dict:
        prompt = f"""
        You are an expert Resume Intelligence Agent. Extract and structure information from the resume text.
        Return a JSON object with:
        - personal_info (dict: name, email, phone)
        - summary (string: brief professional summary)
        - skills (list of strings)
        - education (list of dicts: degree, university, year)
        - experience (list of dicts: role, company, duration, description)
        - projects (list of dicts: name, technologies, description)
        - certifications (list of strings)

        Resume Text:
        {resume_text}
        """
        return self._call_llm(prompt)
