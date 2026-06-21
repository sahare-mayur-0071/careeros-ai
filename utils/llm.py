import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from utils.logger import setup_logger

load_dotenv()
logger = setup_logger(__name__)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_llm_response(prompt: str, model_name: str = "gemini-1.5-flash", temperature: float = 0.2, expect_json: bool = True):
    try:
        model = genai.GenerativeModel(model_name)
        generation_config = genai.types.GenerationConfig(temperature=temperature)
        if expect_json:
            generation_config.response_mime_type = "application/json"
            
        response = model.generate_content(prompt, generation_config=generation_config)
        text_response = response.text
        
        if expect_json:
            try:
                # Clean up markdown code blocks if present
                if text_response.startswith("```json"):
                    text_response = text_response.replace("```json\\n", "").replace("\\n```", "")
                elif text_response.startswith("```"):
                    text_response = text_response.replace("```\\n", "").replace("\\n```", "")
                    
                return json.loads(text_response)
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing error: {e}\\nRaw: {text_response}")
                return None
                
        return text_response
    except Exception as e:
        logger.error(f"LLM API error: {e}")
        return None
