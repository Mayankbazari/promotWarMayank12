"""Medical Agent — provides medical emergency guidance."""

from __future__ import annotations

from agents.base import call_gemini_typed
from models.schemas import MedicalResult


MEDICAL_PROMPT = """You are a certified medical emergency response expert with extensive \
training in pre-hospital care and emergency medicine.

## Task
Analyze the medical emergency described below and provide structured, actionable guidance \
that a bystander can follow BEFORE professional help arrives.

## Emergency Description
"{text}"

## Response Guidelines
1. **condition**: Identify the most likely medical condition (be specific but understandable)
2. **actions**: Provide 3-6 clear, numbered first-aid actions in order of priority:
   - Start with the most critical/time-sensitive action
   - Use simple language a non-medical person can follow
   - Include relevant emergency numbers (ambulance: 108)
   - Include DO NOTs where critical (e.g., "Do NOT give water if unconscious")
3. **risk**: Rate as "critical", "high", "medium", or "low"
   - "critical": Immediate life threat requiring instant action
   - "high": Serious risk if untreated within minutes
   - "medium": Needs attention but not immediately life-threatening
   - "low": Minor issue, basic first aid sufficient

## Output
Return ONLY valid JSON — no markdown, no explanation:
{{
  "condition": "<identified_condition>",
  "actions": [
    "Action 1",
    "Action 2",
    "Action 3"
  ],
  "risk": "<risk_level>"
}}"""


def handle_medical(text: str) -> MedicalResult:
    """Generate medical emergency response guidance.

    Args:
        text: Description of the medical emergency.

    Returns:
        MedicalResult with condition, actions, and risk level.
    """
    prompt = MEDICAL_PROMPT.format(text=text)
    return call_gemini_typed(prompt, MedicalResult, temperature=0.2)
