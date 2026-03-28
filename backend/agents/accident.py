"""Accident Agent — provides accident response guidance."""

from __future__ import annotations

from agents.base import call_gemini_typed
from models.schemas import AccidentResult


ACCIDENT_PROMPT = """You are a certified accident response and trauma care expert with \
extensive training in roadside emergency response and workplace safety.

## Task
Analyze the accident described below and provide structured, actionable guidance \
that a bystander can follow BEFORE professional help arrives.

## Accident Description
"{text}"

## Response Guidelines
1. **actions**: Provide 3-6 clear, ordered first-response actions:
   - Prioritize scene safety (e.g., move away from traffic, turn off engine)
   - Include ABCs of emergency care (Airway, Breathing, Circulation)
   - Include relevant emergency numbers (ambulance: 108, police: 100)
   - Include critical DO NOTs (e.g., "Do NOT move someone with a potential spinal injury")
   - Keep instructions simple enough for untrained bystanders
2. **risk**: Rate as "critical", "high", "medium", or "low"
   - "critical": Multiple casualties, severe injuries, ongoing danger
   - "high": Serious single injury, risk of worsening
   - "medium": Moderate injuries, scene is stable
   - "low": Minor incident, no significant injuries

## Output
Return ONLY valid JSON — no markdown, no explanation:
{{
  "actions": [
    "Action 1",
    "Action 2",
    "Action 3"
  ],
  "risk": "<risk_level>"
}}"""


def handle_accident(text: str) -> AccidentResult:
    """Generate accident response guidance.

    Args:
        text: Description of the accident.

    Returns:
        AccidentResult with actions and risk level.
    """
    prompt = ACCIDENT_PROMPT.format(text=text)
    return call_gemini_typed(prompt, AccidentResult, temperature=0.2)
