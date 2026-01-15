# ai/gemini_utils.py
import logging
from django.conf import settings

logger = logging.getLogger("ai")

# Default model
MODEL_NAME = getattr(settings, "GEMINI_MODEL", "gemini-1.5-flash")

# Make sure GEMINI_API_KEY is set (log at import time without importing heavy SDK)
if not getattr(settings, "GEMINI_API_KEY", None):
    logger.warning("GEMINI_API_KEY is not set. AI features will not work.")


def call_gemini(prompt: str) -> str:
    """
    Calls Google Gemini API with the provided prompt.
    Returns the AI-generated text. Performs lazy import of the SDK so management
    commands and tests don't import large optional dependencies at module import time.
    """
    api_key = getattr(settings, "GEMINI_API_KEY", None)
    if not api_key:
        return "GEMINI_API_KEY is not configured."

    try:
        # Lazy import to avoid heavy imports during manage.py commands
        import google.genai as genai
    except Exception:
        logger.exception("Failed to import google.genai SDK")
        return "AI service is not available."

    try:
        # Create a client
        client = genai.Client(api_key=api_key)

        # Generate content
        response = client.generate_text(
            model=MODEL_NAME,
            prompt=prompt
        )

        # Response is now a dict with 'candidates'
        if response and response.candidates:
            return response.candidates[0].output_text.strip()

        return "No response generated."

    except Exception:
        logger.exception("Gemini API failure")
        return "AI service is temporarily unavailable."












