"""Personalized learning recommendations module."""
from gemini_client import generate

SYSTEM = (
    "You are EduGenie, a learning coach. Build practical, well-structured "
    "study plans for self-learners."
)


def get_learning_recommendations(topic: str) -> str:
    prompt = (
        f"Create a learning path for: {topic}\n\n"
        "Structure it as Beginner, Intermediate, Advanced. For each level give: "
        "topics to learn, an estimated timeline, and 2-3 resources "
        "(videos, articles, or books). End with one practice project idea."
    )
    return generate(prompt, system=SYSTEM)
