import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from utils.logger import console, log_trace
from tools.pdf_parser import extract_text_from_pdf
from tools.jd_parser import extract_text_from_url
from guardrails.pii_scrubber import scrub_pii
from agent.coordinator import AgentCoordinator

def main():
    load_dotenv()
    console.print("[bold green]🚀 Welcome to Career Copilot v0![/bold green]")
    log_trace("System", "Career Copilot CLI started.")
    
    # 1. Initialize
    with console.status("[bold blue]Initializing agent...[/bold blue]"):
        try:
            agent = AgentCoordinator()
            log_trace("Init", "Agent components loaded.")
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            return
            
    # 2. Ingest Data
    pdf_path = console.input("[bold cyan]Enter path to CV (PDF): [/bold cyan]").strip()
    jd_url = console.input("[bold cyan]Enter Job Description URL: [/bold cyan]").strip()
    
    if not os.path.exists(pdf_path):
        console.print("[bold red]PDF file not found![/bold red]")
        return
        
    with console.status("[bold blue]Parsing and scrubbing documents...[/bold blue]"):
        try:
            raw_cv = extract_text_from_pdf(pdf_path)
            safe_cv = scrub_pii(raw_cv)
            
            raw_jd = extract_text_from_url(jd_url)
        except Exception as e:
            console.print(f"[bold red]Data Ingestion Error:[/bold red] {e}")
            return
            
    console.print("[bold green]Documents processed securely![/bold green]")
    
    # 3. Analyze
    with console.status("[bold blue]Agent is thinking (Chain-of-Thought)...[/bold blue]"):
        result = agent.analyze_fit(safe_cv, raw_jd)
        
    # 4. Display Results
    console.print("\n[bold yellow]--- Analysis Results ---[/bold yellow]")
    if "error" in result:
        console.print(f"[red]{result['error']}[/red]")
    else:
        console.print(f"⭐ [bold]Fit Score:[/bold] {result.get('overall_fit_score')}/100")
        console.print("\n🔍 [bold]Missing Skills:[/bold]")
        for skill in result.get('missing_skills', []):
            console.print(f"  - {skill}")
        console.print("\n💡 [bold]Recommendations:[/bold]")
        for rec in result.get('recommendations', []):
            console.print(f"  - {rec}")
            
    # 5. Interactive Memory Loop
    console.print("\n[bold cyan]You can now ask follow-up questions (Type 'exit' to quit):[/bold cyan]")
    while True:
        try:
            user_input = console.input("\n[bold magenta]You:[/bold magenta] ").strip()
            if user_input.lower() in ['exit', 'quit']:
                break
                
            with console.status("[bold blue]Agent is replying...[/bold blue]"):
                response = agent.send_message(user_input)
                
            console.print(f"[bold green]Copilot:[/bold green] {response}")
            
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
