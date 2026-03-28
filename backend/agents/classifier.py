"""Emergency Classifier Agent — categorizes the emergency type and severity.

This module uses Google Gemini to process free-form emergency descriptions
and return highly structured, valid JSON classification results.
"""

from __future__ import annotations

import logging
from agents.base import call_gemini_typed
from models.schemas import ClassificationResult

# Configure module logger
logger = logging.getLogger(__name__)


CLASSIFIER_PROMPT = """You are an expert emergency classifier with training in medical triage, \
accident assessment, and disaster response.

## Task
Analyze the following emergency description and classify it accurately.

## Input
Emergency description: "{text}"

## Classification Rules
1. **type** — Classify into exactly ONE of: "medical", "accident", "fire", "unknown"
   - "medical": Health emergencies (chest pain, breathing difficulty, poisoning, seizure, etc.)
   - "accident": Vehicle crashes, falls, workplace injuries, drowning, etc.
   - "fire": Fire-related emergencies, gas leaks with fire risk, explosions
   - "unknown": Cannot determine the emergency type from the description

2. **severity** — Rate as ONE of: "critical", "high", "medium", "low"
   - "critical": Immediate life threat (cardiac arrest, severe bleeding, unconsciousness)
   - "high": Serious but not immediately fatal (chest pain, major fractures, burns)
   - "medium": Needs medical attention but stable (minor fractures, moderate pain)
   - "low": Non-urgent (minor cuts, mild symptoms)

3. **confidence** — A float between 0.0 and 1.0 indicating classification confidence

## Output
Return ONLY valid JSON matching this schema:
{{
  "type": "<emergency_type>",
  "severity": "<severity_level>",
  "confidence": <0.0-1.0>
}}"""


def classify_emergency(text: str) -> ClassificationResult:
    """Classify an emergency from free-text description using Gemini AI.

    Args:
        text (str): User's description of the emergency (e.g. "Car crash on highway").

    Returns:
        ClassificationResult: Typed object with type, severity, and confidence score.

    Raises:
        RuntimeError: If the AI agent pipeline fails after multiple retries.
    """
    logger.info("🚦 Classifying emergency text (length: %d)", len(text))
    prompt = CLASSIFIER_PROMPT.format(text=text)
    return call_gemini_typed(prompt, ClassificationResult, temperature=0.1)
