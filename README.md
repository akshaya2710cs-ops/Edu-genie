# 🎓 EduGenie – Gemini Powered Learning Assistant

FastAPI backend + HTML/CSS/JS frontend + Google Gemini API.

Features: Q&A • Concept Explanation • Quiz (3 MCQs) • Summarizer • Learning Path

## Folder structure
```
EduGenie/
├── main.py                 # FastAPI app + routes
├── gemini_client.py        # Gemini API helper
├── qna.py                  # Question answering
├── explanation_module.py   # Concept explanation
├── quiz_module.py          # Quiz generation (JSON)
├── summary_module.py       # Summarization
├── learning_path.py        # Learning recommendations
├── templates/index.html    # Frontend page
├── static/style.css, script.js
├── requirements.txt
├── render.yaml             # Render deployment config
└── .env.example
```

## Run locally (VS Code)
1. Open the folder in VS Code → Terminal → New Terminal
2. Create a virtual environment
   - Windows PowerShell: `python -m venv venv`, then run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and `.\venv\Scripts\Activate.ps1` in the same terminal. This policy change applies only to the current terminal session.
   - Windows Command Prompt: `python -m venv venv` then `venv\Scripts\activate.bat`
   - Mac/Linux: `python3 -m venv venv` then `source venv/bin/activate`
3. Install dependencies: Windows: `python -m pip install -r requirements.txt`; Mac/Linux: `python3 -m pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and paste your Gemini API key
   (free key: https://aistudio.google.com/apikey)
5. Start the app: Windows: `python -m uvicorn main:app --reload`; Mac/Linux: `python3 -m uvicorn main:app --reload`
6. Open http://127.0.0.1:8000  (API docs: http://127.0.0.1:8000/docs)

## Deploy on Render
1. Push this folder to a GitHub repo (**do not upload `.env`**)
2. Render → New + → Web Service → connect the repo
3. Settings:
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Environment tab → add `GEMINI_API_KEY` = your key
5. Deploy. (Free plan sleeps after inactivity – first load may take ~30-60 sec.)
