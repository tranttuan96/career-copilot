import PyPDF2
from utils.logger import log_trace

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text content from a PDF file."""
    log_trace("Tool: pdf_parser", f"Extracting text from {file_path}")
    text = ""
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        log_trace("Tool: pdf_parser", f"Successfully extracted {len(text)} characters.")
        return text.strip()
    except Exception as e:
        log_trace("Tool Error: pdf_parser", str(e))
        raise Exception(f"Failed to read PDF: {e}")
