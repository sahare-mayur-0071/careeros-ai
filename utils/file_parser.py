import os
import pdfplumber
from PIL import Image
from google import genai
from utils.logger import setup_logger

logger = setup_logger(__name__)

def parse_pdf(pdf_file) -> str:
    """Extract text from a PDF file robustly."""
    try:
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    except Exception as e:
        logger.error(f"Error parsing PDF: {e}")
        return ""

def parse_image(image_path: str) -> str:
    """Extract text from a resume image using Gemini 2.5 Flash."""
    try:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        image = Image.open(image_path)
        response = client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=['Extract all the text from this resume precisely. Output only the extracted text.', image]
        )
        return response.text
    except Exception as e:
        logger.error(f"Error parsing image: {e}")
        return ""
