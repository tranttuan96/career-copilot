# Career Copilot v0

A personal AI career assistant that reads Job Descriptions (JDs) and tailored CVs to provide fit evaluation and improvement suggestions. This is the v0 implementation for the Kaggle 5-Day AI Agents capstone.

## Features (5 Core Concepts)
1. **Agent Architecture**: Chain-of-Thought reasoning with structured JSON outputs.
2. **Evaluation**: LLM-as-a-Judge validation script.
3. **Guardrails**: PII (Personally Identifiable Information) removal before LLM processing.
4. **Memory**: Short-term conversational memory within the CLI session.
5. **Tools**: PDF CV parser and web JD parser.

## Setup
1. Clone the repository.
2. Run `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and configure your API keys.
4. Run `python src/main.py` to start the CLI.

## Observability
- **UX**: The terminal shows clean progress spinners for a good user experience.
- **Trace Logs**: All LLM chains, prompts, and tool executions are fully logged in `logs/agent_trace.log` for transparency and explainability.
