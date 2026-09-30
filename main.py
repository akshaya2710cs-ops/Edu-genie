"""EduGenie - Gemini powered learning assistant (FastAPI backend)."""
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from explanation_module import explain_concept
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="EduGenie", description="Gemini powered learning assistant")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


class TextInput(BaseModel):
    text: str = Field(..., min_length=2, max_length=8000)


def run(func, text: str) -> str | list:
    try:
        return func(text.strip())
    except (RuntimeError, ValueError) as exc:
        raise HTTPException(status_code=502, detail=str(exc))


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/qa")
def qa(body: TextInput):
    return {"result": run(answer_question, body.text)}


@app.post("/explain")
def explain(body: TextInput):
    return {"result": run(explain_concept, body.text)}


@app.post("/quiz")
def quiz(body: TextInput):
    return {"result": run(generate_quiz, body.text)}


@app.post("/summarize")
def summarize(body: TextInput):
    return {"result": run(summarize_text, body.text)}


@app.post("/learn/recommendations")
def recommendations(body: TextInput):
    return {"result": run(get_learning_recommendations, body.text)}
