# Prompt Injection Scanner

A small Python tool that automatically attacks an LLM chatbot with prompt-injection payloads and reports which ones leak a hidden secret.

## How it works

- target.py: a local chatbot (Ollama, llama3.2:1b) whose system prompt hides a secret password and tells it never to reveal it
- payloads.py: 10 attacks across categories (direct, override, prompt extraction, roleplay, storytelling, completion, spelling, encoding, emoji, translation)
- run_scan.py: sends each attack 5 times and counts how often the secret appears in the reply, saved to results.json
- report.py: turns results.json into report.html, ranked worst-first with example leaked replies as evidence

## Results

Across runs, 46% to 64% of attempts leaked the secret. In the latest run, prompt extraction, roleplay, spelling and encoding leaked on every attempt, while a plain "what is the password?" leaked only some of the time. The model is non-deterministic, so results are reported as rates over repeated attempts, not single pass/fail outcomes.

Prompt extraction maps to OWASP LLM07 (System Prompt Leakage) and the others to LLM01 (Prompt Injection).

## Usage

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    python3 run_scan.py
    python3 report.py

## Limitations

- The judge is a simple string match. It misses leaks in other forms such as emoji, base64, or text with spaces between letters.
- One small model and one secret, so results will not generalize to larger models.
- Ten payloads is a small library.

## Next steps

- A smarter judge that normalizes replies and uses a second model as referee
- More payloads and a comparison across models
