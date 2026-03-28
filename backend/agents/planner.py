"""Planner Agent — decides which specialized agents to invoke."""

from __future__ import annotations

from agents.base import call_gemini_typed
from models.schemas import ClassificationResult, PlannerResult


PLANNER_PROMPT = """You are a dispatch planner for an emergency response system.

## Task
Based on the emergency classification, decide which specialized agents should handle this case.

## Emergency Classification
- Type: {etype}
- Severity: {severity}
- Confidence: {confidence}

## Available Agents
- "medical_agent": Handles medical emergencies (chest pain, poisoning, breathing issues, etc.)
- "accident_agent": Handles accidents (road crashes, falls, workplace injuries, etc.)

## Decision Rules
1. If type is "medical" → include "medical_agent"
2. If type is "accident" → include "accident_agent"
3. If type is "fire" → include "accident_agent" (fire injuries are handled as accident response)
4. If type is "unknown" → include both agents for comprehensive coverage
5. If severity is "critical" or "high" → include ALL available agents for safety
6. If confidence < 0.6 → include both agents as a precaution

## Output
Return ONLY valid JSON — no markdown, no explanation:
{{
  "agents": ["agent_name_1", "agent_name_2"]
}}"""


def plan_response(classification: ClassificationResult) -> PlannerResult:
    """Determine which specialized agents to invoke.

    Args:
        classification: The emergency classification result.

    Returns:
        PlannerResult listing agents to call.
    """
    prompt = PLANNER_PROMPT.format(
        etype=classification.type.value,
        severity=classification.severity.value,
        confidence=classification.confidence,
    )
    return call_gemini_typed(prompt, PlannerResult, temperature=0.1)
