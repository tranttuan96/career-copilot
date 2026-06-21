import os
import sys
import json
from google import genai

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from utils.logger import console
from agent.coordinator import AgentCoordinator
from guardrails.pii_scrubber import scrub_pii

JUDGE_PROMPT = """You are an impartial AI Judge.
Your task is to evaluate whether a Career Assistant Agent correctly identified the missing skills from a candidate's CV based on a Job Description (JD).

Given the True Expected Missing Skills, compare them to the Agent's Predicted Missing Skills.
It is a PASS if the Agent caught the core expected skills (minor wording differences are acceptable).
It is a FAIL if the Agent hallucinated completely irrelevant skills or missed the most critical ones.

Output JSON only in this exact format:
{
  "score": "PASS" or "FAIL",
  "reason": "Brief explanation"
}
"""

def main():
    load_dotenv()
    console.print("[bold green]🧪 Starting LLM-as-a-Judge Evaluation Suite...[/bold green]")
    
    try:
        agent = AgentCoordinator()
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        judge_chat = client.chats.create(model="gemini-2.5-flash")
    except Exception as e:
        console.print(f"[bold red]Setup Error:[/bold red] {e}")
        return
    
    # Load cases
    cases_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tests", "eval_cases.json")
    try:
        with open(cases_path, "r", encoding="utf-8") as f:
            cases = json.load(f)
    except Exception as e:
        console.print(f"[bold red]Failed to load test cases:[/bold red] {e}")
        return
        
    pass_count = 0
    total = len(cases)
    
    for case in cases:
        console.print(f"\n[bold cyan]Evaluating Case: {case['id']}[/bold cyan]")
        
        with console.status("[bold blue]Running Agent and Judge...[/bold blue]"):
            # 1. Scrub CV
            safe_cv = scrub_pii(case['cv_text'])
            
            # 2. Run Agent
            result = agent.analyze_fit(safe_cv, case['jd_text'])
            predicted_skills = result.get("missing_skills", [])
            
            # 3. Judge Evaluation
            judge_input = (
                f"System: {JUDGE_PROMPT}\n\n"
                f"Expected Missing Skills: {case['expected_missing_skills']}\n"
                f"Agent's Predicted Missing Skills: {predicted_skills}\n"
            )
            
            try:
                judge_response = judge_chat.send_message(judge_input).text
                clean_json = judge_response.replace("```json", "").replace("```", "").strip()
                judge_result = json.loads(clean_json)
                
                score = judge_result.get("score")
                reason = judge_result.get("reason")
                
                if score == "PASS":
                    pass_count += 1
                    console.print(f"[bold green]✅ PASS[/bold green] - {reason}")
                else:
                    console.print(f"[bold red]❌ FAIL[/bold red] - {reason}")
                    
            except Exception as e:
                console.print(f"[bold red]Judge LLM Error:[/bold red] {e}")

    console.print(f"\n[bold yellow]🏆 Final Score: {pass_count}/{total} cases passed.[/bold yellow]")

if __name__ == "__main__":
    main()
