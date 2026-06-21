import requests
from bs4 import BeautifulSoup
from utils.logger import log_trace

def extract_text_from_url(url: str) -> str:
    """Fetch URL and extract the main text content."""
    log_trace("Tool: jd_parser", f"Fetching URL: {url}")
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove script and style elements
        for script_or_style in soup(['script', 'style', 'header', 'footer', 'nav']):
            script_or_style.decompose()
            
        text = soup.get_text(separator='\n')
        # Clean up empty lines
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = '\n'.join(chunk for chunk in chunks if chunk)
        
        log_trace("Tool: jd_parser", f"Successfully extracted {len(clean_text)} characters.")
        return clean_text
    except Exception as e:
        log_trace("Tool Error: jd_parser", str(e))
        raise Exception(f"Failed to fetch JD from URL: {e}")
