import logging
import os
from datetime import datetime
from rich.console import Console

# UX Console for user-facing spinners and clean prints
console = Console()

def setup_trace_logger():
    """Sets up the file logger for Observability/Tracing."""
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    log_filename = f"logs/agent_trace_{datetime.now().strftime('%Y%m%d')}.log"
    
    logger = logging.getLogger("CareerCopilotTrace")
    logger.setLevel(logging.DEBUG)
    
    # Avoid adding multiple handlers if already set up
    if not logger.handlers:
        fh = logging.FileHandler(log_filename, encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        
        formatter = logging.Formatter('%(asctime)s - [%(levelname)s] - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        
    return logger

# Global trace logger instance
trace_logger = setup_trace_logger()

def log_trace(step: str, details: str):
    """Log internal agent traces to the file without spamming the terminal."""
    trace_logger.debug(f"{step}:\n{details}\n{'-'*40}")
