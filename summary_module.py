"""Summarization module."""
from gemini_client import generate

SYSTEM = (
    "You are EduGenie, a study assistant. Summarize educational text so it is "
    "short, accurate, and easy to revise. Do not add facts that are not in the text."
)


def summarize_text(text: str) -> str:
    prompt = (
        "Summarize the following passage. Give a 2-3 sentence summary, then "
        f"3-5 key points as bullets.\n\nPassage:\n{text}"
    )
    return generate(prompt, system=SYSTEM)
