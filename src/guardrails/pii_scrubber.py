import re
from utils.logger import log_trace

def scrub_pii(text: str) -> str:
    """Detect and redact PII such as Emails and Phone numbers from text."""
    # Regex for Email
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    text = re.sub(email_pattern, '[REDACTED_EMAIL]', text)
    
    # Regex for Phone numbers (Basic international/local patterns)
    # Matches formats like: +1234567890, (123) 456-7890, 123-456-7890, 0987654321
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?(\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}'
    text = re.sub(phone_pattern, '[REDACTED_PHONE]', text)
    
    log_trace("Guardrail: PII Scrubber", "Scrubbed PII from text.")
    return text
