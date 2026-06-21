import os
import sys

# Add src to the Python path so absolute imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from utils.logger import console, log_trace

def main():
    load_dotenv()
    console.print("[bold green]🚀 Welcome to Career Copilot v0![/bold green]")
    log_trace("System", "Career Copilot CLI started.")
    
    # Placeholder for Phase 2 and 3
    with console.status("[bold blue]Initializing agent...[/bold blue]"):
        import time
        time.sleep(1)
        log_trace("Init", "Agent components loaded.")
        
    console.print("[bold cyan]Agent is ready. (Phase 1 Setup Complete)[/bold cyan]")

if __name__ == "__main__":
    main()
