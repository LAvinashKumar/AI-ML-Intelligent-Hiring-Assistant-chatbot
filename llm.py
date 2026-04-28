"""
LLM interface for TalentScout using Google Gemini.
Handles model initialization and chat completions.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT

load_dotenv()


def get_model():
    """Initialize and return the Gemini model."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(
        model_name="gemini-2.0-flash",
        system_instruction=SYSTEM_PROMPT,
        generation_config=genai.GenerationConfig(
            temperature=0.7,
            max_output_tokens=1024,
        ),
    )


def build_gemini_history(messages: list[dict]) -> list[dict]:
    """
    Convert our internal message format to Gemini's expected history format.
    Gemini expects: [{"role": "user"|"model", "parts": [{"text": "..."}]}]
    """
    history = []
    for msg in messages:
        role = "model" if msg["role"] == "assistant" else "user"
        history.append({
            "role": role,
            "parts": [{"text": msg["content"]}]
        })
    return history


def get_response(messages: list[dict]) -> str:
    """
    Send conversation history to Gemini and return the assistant's reply.

    Args:
        messages: List of {"role": "user"|"assistant", "content": "..."} dicts.

    Returns:
        The model's text response.
    """
    try:
        model = get_model()

        if not messages:
            return "Hello! I'm having trouble starting the conversation. Please refresh and try again."

        # Split history (all but last) from the latest user message
        history = build_gemini_history(messages[:-1])
        last_message = messages[-1]["content"]

        chat = model.start_chat(history=history)
        response = chat.send_message(last_message)
        return response.text

    except ValueError as e:
        return f"⚠️ Configuration Error: {str(e)}"
    except Exception as e:
        error_msg = str(e)
        if "API_KEY" in error_msg.upper() or "401" in error_msg:
            return "⚠️ Invalid API key. Please check your GEMINI_API_KEY in the .env file."
        if "quota" in error_msg.lower() or "429" in error_msg:
            return "⚠️ API quota exceeded. Please wait a moment and try again."
        return f"⚠️ An error occurred: {error_msg}"
