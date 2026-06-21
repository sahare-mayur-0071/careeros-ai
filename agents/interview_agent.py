from agents.base_agent import BaseAgent
import json

class InterviewCoachAgent(BaseAgent):
    def __init__(self):
        super().__init__("Interview Coach Agent", "Generates custom interview questions.")

    def generate(self, parsed_resume: dict, target_role: str) -> dict:
        prompt = f"""
        You are an Interview Coach Agent. Create targeted interview questions for a {target_role} based on their resume.
        Return a JSON object with:
        - technical_questions (list of dicts: question, expected_answer_points (list of strings))
        - hr_questions (list of dicts: question, expected_answer_points)
        - behavioral_questions (list of dicts: question, expected_answer_points)
        - project_discussion_questions (list of dicts: question, expected_answer_points)

        Parsed Resume:
        {json.dumps(parsed_resume, indent=2)}
        """
        return self._call_llm(prompt)
