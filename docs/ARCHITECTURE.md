# System Architecture

Career Copilot v0 is built with a highly decoupled architecture designed to demonstrate 5 core AI Agent concepts required for the Kaggle Capstone.

## 1. Agent Architecture (LLM + Logic)
The core of the system is in `src/agent/coordinator.py`. 
- **LLM Engine**: We use Google Gemini 2.5 Flash via the `google-genai` SDK.
- **Chain-of-Thought (CoT)**: In `prompts.py`, the System Prompt explicitly forces the LLM to think step-by-step (`"reasoning"` field) before providing the final answer. This reduces hallucinations.
- **Structured Output**: We enforce a strict JSON output format. This is crucial for down-stream tasks (e.g., when moving to React/NestJS in future phases, the backend needs predictable JSON, not plain text).

## 2. Guardrails (Data Privacy)
Before any data reaches the LLM, it must pass through our Guardrails (`src/guardrails/pii_scrubber.py`).
- **PII Scrubbing**: We use Regular Expressions to scan the raw CV text.
- **Redaction**: Any Email or Phone number found is replaced with `[REDACTED_EMAIL]` and `[REDACTED_PHONE]`. 
- **Why?**: This prevents sensitive Personal Identifiable Information (PII) from being sent to external third-party LLM APIs, ensuring compliance and privacy.

## 3. Tools (Information Retrieval)
Agents need to interact with the outside world. We built two basic tools:
- **PDF Parser (`src/tools/pdf_parser.py`)**: Uses `PyPDF2` to extract raw text from candidate CVs.
- **JD Parser (`src/tools/jd_parser.py`)**: Uses `requests` and `BeautifulSoup` to scrape Job Descriptions from web URLs and clean up the HTML noise (scripts, styles, navbars).

## 4. Memory (Context Retention)
The Agent Coordinator maintains an active `ChatSession` object (`self.chat = self.client.chats.create()`). 
- When the user asks follow-up questions in the CLI loop (`main.py`), the Agent remembers the previous CV, JD, and the Analysis it just generated.
- This represents **Short-term memory**.

## 5. Evaluation (LLM-as-a-Judge)
Testing non-deterministic LLMs is hard. We implemented `src/evaluate.py`:
- We have predefined test cases (`tests/eval_cases.json`) with known "Expected Missing Skills".
- We run the Agent to get "Predicted Missing Skills".
- A separate LLM instance (the "Judge") is prompted to compare the Expected vs Predicted skills and output a `PASS` or `FAIL`. This is the **Evaluation-Driven Development** approach.
