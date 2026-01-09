import google.generativeai as genai
from django.conf import settings
import logging

logger = logging.getLogger("ai")

genai.configure(api_key=settings.GEMINI_API_KEY)

MODEL_NAME = getattr(settings, "GEMINI_MODEL", "gemini-1.5-flash")


def call_gemini(prompt: str) -> str:
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)

        if response and hasattr(response, "text"):
            return response.text.strip()

        return "No response generated."

    except Exception:
        logger.exception("Gemini API failure")
        return "AI service is temporarily unavailable."




























































# import google.genai as genai
# from django.conf import settings
# import logging

# # Dedicated AI logger
# logger = logging.getLogger("ai")

# # -------------------------------------------------
# # Gemini Configuration
# # -------------------------------------------------
# try:
#     genai.configure(api_key=settings.GEMINI_API_KEY)
#     logger.info("Gemini API configured successfully.")
# except Exception as e:
#     logger.error("Gemini initialization failed", exc_info=True)

# MODEL_NAME = getattr(settings, "GEMINI_MODEL", "gemini-1.5-flash")

# # -------------------------------------------------
# # Safe Wrapper for all AI calls
# # -------------------------------------------------
# def call_gemini(prompt: str) -> str:
#     try:
#         MODEL = genai.GenerativeModel(MODEL_NAME)
#         response = MODEL.generate_content(prompt)

#         if hasattr(response, "text") and response.text:
#             return response.text.strip()

#         logger.warning("Empty AI response.")
#         return "The AI could not generate a response."

#     except Exception as e:
#         logger.error("Gemini API Error", exc_info=True)
#         return "AI service unavailable. Please try again."






















