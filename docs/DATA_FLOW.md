# Data Flow and Observability

To master this repository, it is critical to understand how data flows through the application and how you can observe the internal "thoughts" of the Agent.

## Data Flow Pipeline

1. **Input**: User provides a path to a local PDF (CV) and a URL (Job Description).
2. **Parsing**:
   - `pdf_parser` reads the PDF and converts it to a raw string.
   - `jd_parser` fetches the URL, strips HTML, and returns a clean string.
3. **Guardrail Intervention**:
   - The raw CV string is passed through `pii_scrubber`.
   - Output is a "Safe CV" string (PII removed).
4. **Agent Analysis**:
   - `coordinator.analyze_fit()` injects the Safe CV and Clean JD into the Prompt.
   - The LLM processes the Prompt and returns a JSON string.
5. **Output**:
   - The JSON string is parsed into a Python dictionary.
   - The UI (`rich` console) displays the score, missing skills, and recommendations.

## Observability (Transparency & Tracing)

In AI Engineering, you must separate **User Experience (UX)** from **Observability**.

- **UX**: The terminal uses `rich` spinners. The user only sees clean UI like *"Agent is thinking..."* and the final results. We do not spam the terminal with huge prompts.
- **Observability**: Developers need to see everything. This is handled by `src/utils/logger.py`.
  - Every single step is logged into `logs/agent_trace_YYYYMMDD.log`.
  - **What is logged?**
    - The exact text extracted by tools.
    - Any tool errors.
    - The exact prompt sent to the LLM (`Message IN`).
    - The exact raw output from the LLM (`Message OUT`), including the Chain-of-Thought reasoning.

### How to use the Trace Log to learn:
After running the app, open `logs/agent_trace_*.log`. Look for `Agent: Message OUT`. You will see the `"reasoning"` field where the LLM explains *why* it chose the missing skills. This is how you verify that the Chain-of-Thought is working correctly!
