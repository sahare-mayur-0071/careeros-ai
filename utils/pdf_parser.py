import pdfplumber
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
                    text += page_text + "\\n"
        return text
    except Exception as e:
        logger.error(f"Error parsing PDF: {e}")
        return ""
