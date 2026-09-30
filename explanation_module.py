"""Concept explanation module (simplified explanations)."""
from gemini_client import generate

SYSTEM = (
    "You are EduGenie, a teacher who explains complex ideas to beginners. "
    "Use very simple words, a real-life analogy, and a short example."
)


def explain_concept(topic: str) -> str:
    prompt = (
        f"Explain this concept in a simple way for a beginner: {topic}\n\n"
        "Format: 1) One-line definition 2) Simple explanation 3) Real-life analogy "
        "4) A small example."
    )
    return generate(prompt, system=SYSTEM)
