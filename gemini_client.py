"""Shared Gemini helper used by every module."""
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

_client = None

# Tries the primary model first, then falls back if it is unavailable.
PRIMARY_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
FALLBACK_MODELS = ["gemini-2.5-flash"]


def _get_client() -> genai.Client:
    global _client
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Add it to your .env file (local) "
            "or to Environment Variables (Render)."
        )
    if _client is None:
        _client = genai.Client(api_key=api_key)
    return _client


def generate(prompt: str, system: str | None = None, json_mode: bool = False) -> str:
    """Send a prompt to Gemini and return the text reply."""
    client = _get_client()
    config = types.GenerateContentConfig(
        system_instruction=system,
        temperature=0.4,
        response_mime_type="application/json" if json_mode else None,
    )
    last_error = None
    for model in dict.fromkeys([PRIMARY_MODEL, *FALLBACK_MODELS]):
        try:
            response = client.models.generate_content(
                model=model, contents=prompt, config=config
            )
            if response.text:
                return response.text.strip()
        except Exception as exc:  # try next model
            last_error = exc
    raise RuntimeError(f"Gemini request failed: {last_error}")
