"""Pydantic schemas for request/response validation."""

from __future__ import annotations

from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, Field


# ──────────────────────────── Enums ────────────────────────────


class EmergencyType(str, Enum):
    MEDICAL = "medical"
    ACCIDENT = "accident"
    FIRE = "fire"
    UNKNOWN = "unknown"


class SeverityLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class RiskLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


# ──────────────────────────── Request ────────────────────────────


class EmergencyInput(BaseModel):
    """User input describing the emergency."""

    text: str = Field(
        ...,
        min_length=3,
        max_length=2000,
        description="Description of the emergency situation",
        examples=["My father has chest pain and sweating"],
    )


# ──────────────────────────── Agent Responses ────────────────────────────


class ClassificationResult(BaseModel):
    """Output of the Emergency Classifier Agent."""

    type: EmergencyType
    severity: SeverityLevel
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str = Field(description="Step-by-step triage reasoning")


class PlannerResult(BaseModel):
    """Output of the Planner Agent."""

    agents: list[str] = Field(
        description="List of specialized agents to invoke"
    )


class MedicalResult(BaseModel):
    """Output of the Medical Agent."""

    condition: str
    actions: list[str]
    risk: RiskLevel


class AccidentResult(BaseModel):
    """Output of the Accident Agent."""

    actions: list[str]
    risk: RiskLevel


# ──────────────────────────── Final Response ────────────────────────────


class EmergencyNumbers(BaseModel):
    """Emergency contact numbers."""

    ambulance: str = "108"
    police: str = "100"
    fire: str = "101"


class AgentAction(BaseModel):
    """Wrapper for any specialized agent result."""

    agent_name: str
    result: Union[MedicalResult, AccidentResult]


class EmergencyResponse(BaseModel):
    """Complete orchestrated response."""

    classification: ClassificationResult
    plan: PlannerResult
    actions: list[AgentAction]
    emergency_numbers: EmergencyNumbers
    summary: Optional[str] = None
