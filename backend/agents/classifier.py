"""Emergency Classifier Agent — categorizes the emergency type and severity."""

from __future__ import annotations

from agents.base import call_gemini_typed
from models.schemas import ClassificationResult


CLASSIFIER_PROMPT = """You are a highly experienced Emergency Dispatcher and Triage Specialist. \
Your task is to analyze emergency reports and provide immediate, accurate classification.

## Guidelines
1. **Analyze First**: Carefully consider the reported situation.
2. **Medical vs. Accident**: 
   - Choose `medical` for health conditions, trauma, poisoning, drowning, or found deceased persons.
   - Choose `accident` for mechanical/vehicle crashes, structural collapses, or work-related physical impacts.
   - If BOTH apply (e.g., car crash with injury), choose `accident` as it implies a rescue operation plus medical aid.
3. **Severity Assessment**: 
   - `critical`: Unconscious, stopped breathing, severe hemorrhage, major vehicle trauma.
   - `high`: Chest pain, breathing difficulty, major fractures.
   - `medium/low`: Stable patients, minor injuries.

## Examples
- Input: "Found person dead on road"
  Output: {"reasoning": "A person found in a suspected non-responsive/deceased state is a critical medical/police matter requiring immediate paramedic protocol.", "type": "medical", "severity": "critical", "confidence": 0.95}
- Input: "Smoke coming from building window"
  Output: {"reasoning": "Active smoke indicates an ongoing fire hazard and potential structure fire.", "type": "fire", "severity": "critical", "confidence": 1.0}
- Input: "Car crashed into a divider, nobody is getting out"
  Output: {"reasoning": "Vehicle impact with potentially trapped or unconscious occupants.", "type": "accident", "severity": "critical", "confidence": 0.98}

## Current Report
Analyze this emergency: "{text}"

## Global Instruction
Respond with ONLY valid JSON matching this schema:
{
  "reasoning": "<thinking through the situation>",
  "type": "medical" | "accident" | "fire" | "unknown",
  "severity": "critical" | "high" | "medium" | "low",
  "confidence": <0.0-1.0>
}"""


def classify_emergency(text: str) -> ClassificationResult:
    """Classify an emergency from free-text description.

    Args:
        text: User's description of the emergency.

    Returns:
        ClassificationResult with type, severity, and confidence.
    """
    prompt = CLASSIFIER_PROMPT.format(text=text)
    return call_gemini_typed(prompt, ClassificationResult, temperature=0.1)
