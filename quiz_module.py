"""Quiz generation module - returns 3 MCQs as structured data."""
import json
import re

from gemini_client import generate

SYSTEM = "You are EduGenie, an exam-question writer. Reply with valid JSON only."


def clean_json_block(text: str) -> str:
    """Remove ```json ... ``` fences if the model adds them."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def generate_quiz(passage: str) -> list[dict]:
    prompt = (
        "Create exactly 3 multiple-choice questions from the topic/text below. "
        "Each question needs exactly 4 plausible options and one correct answer.\n"
        'Return ONLY a JSON array like: [{"question": "...", "options": '
        '["A", "B", "C", "D"], "answer": "<must be identical to one option>"}]\n\n'
        f"Topic/Text:\n{passage}"
    )
    raw = generate(prompt, system=SYSTEM, json_mode=True)
    try:
        data = json.loads(clean_json_block(raw))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Could not parse quiz JSON: {exc}") from exc

    quiz = []
    for item in data[:3]:
        options = [str(o) for o in item.get("options", [])][:4]
        answer = str(item.get("answer", ""))
        if len(options) != 4 or answer not in options:
            continue
        quiz.append({"question": str(item["question"]), "options": options, "answer": answer})
    if not quiz:
        raise ValueError("Quiz generation returned no valid questions. Please try again.")
    return quiz
