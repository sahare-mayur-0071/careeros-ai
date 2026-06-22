import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
import streamlit as st
from utils.logger import setup_logger

load_dotenv()
logger = setup_logger(__name__)

def get_llm_response(prompt: str, model_name: str = "gemini-2.5-flash-lite", temperature: float = 0.2, expect_json: bool = True):
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        
        config_kwargs = {"temperature": temperature}
        if expect_json:
            config_kwargs["response_mime_type"] = "application/json"
            
        config = types.GenerateContentConfig(**config_kwargs)
            
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=config
        )
        text_response = response.text
        
        if expect_json:
            try:
                # Clean up markdown code blocks if present
                if text_response.startswith("```json"):
                    text_response = text_response.replace("```json\n", "").replace("\n```", "")
                elif text_response.startswith("```"):
                    text_response = text_response.replace("```\n", "").replace("\n```", "")
                    
                return json.loads(text_response)
            except json.JSONDecodeError as e:
                logger.error(f"JSON parsing error: {e}\nRaw: {text_response}")
                return None
                
        return text_response
    except Exception as e:
        logger.error(f"LLM API error: {e}")
        st.error(f"LLM API error: {e}")
        return None
