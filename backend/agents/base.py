"""Base agent — shared Gemini client and JSON extraction logic."""

from __future__ import annotations

import json
import logging
import re
from typing import TypeVar

from google import genai
from pydantic import BaseModel

from config import get_settings

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


def _get_client() -> genai.Client:
    """Return a configured Gemini client."""
    settings = get_settings()
    return genai.Client(api_key=settings.GEMINI_API_KEY)


def _extract_json(text: str) -> dict:
    """Extract JSON from LLM response, handling markdown code fences."""
    # Try direct parse first
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try extracting from markdown code block
    match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # Try finding first { ... } block
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Could not extract valid JSON from response: {text[:200]}")


def call_gemini(prompt: str, temperature: float | None = None) -> dict:
    """Call Gemini and return parsed JSON dict.

    Args:
        prompt: The prompt to send.
        temperature: Override default temperature.

    Returns:
        Parsed JSON dictionary from the model response.

    Raises:
        ValueError: If the response cannot be parsed as JSON.
        RuntimeError: If the API call fails after retries.
    """
    settings = get_settings()
    client = _get_client()
    temp = temperature if temperature is not None else settings.AGENT_TEMPERATURE

    for attempt in range(settings.MAX_RETRIES + 1):
        try:
            response = client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
                config={"temperature": temp},
            )
            return _extract_json(response.text)
        except (ValueError, json.JSONDecodeError) as exc:
            logger.warning(
                "Attempt %d/%d — JSON parse error: %s",
                attempt + 1,
                settings.MAX_RETRIES + 1,
                exc,
            )
            if attempt == settings.MAX_RETRIES:
                raise RuntimeError(
                    f"Failed to get valid JSON after {settings.MAX_RETRIES + 1} attempts"
                ) from exc
        except Exception as exc:
            logger.error("Gemini API error: %s", exc)
            if attempt == 1:
                raise RuntimeError(f"Gemini API call failed: {exc}") from exc


def call_gemini_typed(prompt: str, model: type[T], temperature: float | None = None) -> T:
    """Call Gemini and parse the response into a typed Pydantic model.

    Args:
        prompt: The prompt to send.
        model: Pydantic model class to validate against.
        temperature: Override default temperature.

    Returns:
        Validated Pydantic model instance.
    """
    data = call_gemini(prompt, temperature)
    return model(**data)
