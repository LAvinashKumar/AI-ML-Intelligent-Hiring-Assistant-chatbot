# 🤖 TalentScout — AI Hiring Assistant

An intelligent chatbot for initial candidate screening, built for the TalentScout recruitment agency. Powered by Google Gemini and Streamlit.

---

## Project Overview

TalentScout conducts structured, conversational screening interviews for technology roles. It:

- Greets candidates and explains its purpose
- Collects essential info (name, email, phone, experience, role, location)
- Asks candidates to declare their tech stack
- Generates 3–5 tailored technical questions per technology
- Maintains full conversation context throughout
- Gracefully ends the session and summarizes collected data

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| LLM | Google Gemini 1.5 Flash |
| Language | Python 3.10+ |
| Config | python-dotenv |

---

## Installation

### 1. Navigate to the project

```bash
cd talentscout
```

### 2. Install dependencies

```bash
pip3 install google-generativeai python-dotenv
```

For the Streamlit web UI (optional):
```bash
pip3 install streamlit
```

### 3. Set up your API key

Get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

```bash
cp .env.example .env
# Edit .env and paste your key:
# GEMINI_API_KEY=your_key_here
```

### 4. Run the app

**Option A: Simple CLI (no Streamlit needed)**
```bash
python3 simple_chatbot.py
```

**Option B: Web UI with Streamlit**
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Usage Guide

1. The chatbot greets you automatically on load.
2. Confirm consent to begin the screening.
3. Answer each question one at a time.
4. When asked, list your tech stack (e.g., "Python, Django, PostgreSQL, Docker").
5. Answer the generated technical questions.
6. Type `exit`, `quit`, or `stop` at any time to end the session.
7. Use **Start New Session** in the sidebar to reset.

---

## Project Structure

```
talentscout/
├── app.py            # Streamlit UI and conversation orchestration
├── llm.py            # Gemini API integration
├── prompts.py        # System prompt and prompt templates
├── utils.py          # Validation helpers, exit detection
├── requirements.txt
├── .env.example
└── README.md
```

---

## Prompt Design

### System Prompt (`prompts.py`)
A detailed instruction set that:
- Locks the model to the hiring assistant role
- Defines 5 conversation stages (greeting → info gathering → tech stack → questions → wrap-up)
- Enforces one-question-at-a-time behavior
- Handles fallback, validation, and exit detection at the model level

### Context Injection
Before each LLM call, a hidden context note is injected with:
- Current conversation stage
- Already-collected candidate fields

This prevents the model from re-asking answered questions and keeps the flow coherent.

### Technical Question Generation
The system prompt instructs Gemini to generate 3–5 questions per declared technology, varying from easy to advanced, ensuring practical, interview-relevant coverage.

---

## Data Privacy

- Phone numbers and emails are **masked in the sidebar** display.
- No candidate data is persisted to disk or any external service.
- All data lives in Streamlit's in-memory session state and is cleared on refresh.
- The `.env` file (containing the API key) is excluded from version control via `.gitignore`.

---

## Challenges & Solutions

| Challenge | Solution |
|-----------|----------|
| Keeping LLM on-topic | Strong system prompt with explicit role constraints |
| Avoiding repeated questions | Context injection with already-collected fields |
| Exit detection | Keyword matching in `utils.py` before LLM call |
| Gemini history format | Custom `build_gemini_history()` converter in `llm.py` |
| Hiding internal prompts from UI | Filter `GREETING_PROMPT` from rendered chat messages |

---

## Optional Enhancements Implemented

- ✅ Custom dark-theme UI with gradient styling
- ✅ Sidebar with live candidate info (with privacy masking)
- ✅ Session reset button
- ✅ Input validation hints in system prompt
- ✅ Stage-aware context injection

---

## License

MIT
