"""Tests for the Emergency Decision Agent."""

import pytest
from fastapi.testclient import TestClient

from main import app
from models.schemas import (
    ClassificationResult,
    EmergencyType,
    SeverityLevel,
    RiskLevel,
    MedicalResult,
    AccidentResult,
    PlannerResult,
)
from tools.emergency_tools import get_emergency_numbers, get_severity_actions


client = TestClient(app)


# ──────────────────────── Health Check ────────────────────────


def test_health_check():
    """Health endpoint should return 200 with status healthy."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "emergency-decision-agent"


# ──────────────────────── Schema Validation ────────────────────────


def test_classification_schema():
    """ClassificationResult should validate correct data."""
    result = ClassificationResult(
        type=EmergencyType.MEDICAL,
        severity=SeverityLevel.HIGH,
        confidence=0.9,
    )
    assert result.type == EmergencyType.MEDICAL
    assert result.severity == SeverityLevel.HIGH
    assert result.confidence == 0.9


def test_classification_invalid_confidence():
    """ClassificationResult should reject confidence > 1.0."""
    with pytest.raises(Exception):
        ClassificationResult(
            type=EmergencyType.MEDICAL,
            severity=SeverityLevel.HIGH,
            confidence=1.5,
        )


def test_medical_result_schema():
    """MedicalResult should validate correctly."""
    result = MedicalResult(
        condition="possible heart attack",
        actions=["Call ambulance (108)", "Give aspirin if available"],
        risk=RiskLevel.CRITICAL,
    )
    assert result.condition == "possible heart attack"
    assert len(result.actions) == 2
    assert result.risk == RiskLevel.CRITICAL


def test_accident_result_schema():
    """AccidentResult should validate correctly."""
    result = AccidentResult(
        actions=["Check breathing", "Do not move spine", "Call ambulance (108)"],
        risk=RiskLevel.HIGH,
    )
    assert len(result.actions) == 3
    assert result.risk == RiskLevel.HIGH


def test_planner_result_schema():
    """PlannerResult should accept agent list."""
    result = PlannerResult(agents=["medical_agent", "accident_agent"])
    assert "medical_agent" in result.agents


# ──────────────────────── Tools ────────────────────────


def test_emergency_numbers():
    """get_emergency_numbers should return known numbers."""
    numbers = get_emergency_numbers()
    assert numbers.ambulance == "108"
    assert numbers.police == "100"
    assert numbers.fire == "101"


def test_severity_actions_critical():
    """Critical severity should return immediate action guidance."""
    actions = get_severity_actions(SeverityLevel.CRITICAL)
    assert len(actions) > 0
    assert "IMMEDIATELY" in actions[0]


def test_severity_actions_low():
    """Low severity actions should be non-urgent."""
    actions = get_severity_actions(SeverityLevel.LOW)
    assert len(actions) > 0
    assert "Monitor" in actions[0]


# ──────────────────────── Input Validation ────────────────────────


def test_analyze_empty_input():
    """Empty input should return 422."""
    response = client.post("/analyze", json={"text": ""})
    assert response.status_code == 422


def test_analyze_short_input():
    """Too-short input should return 422."""
    response = client.post("/analyze", json={"text": "hi"})
    assert response.status_code == 422


def test_analyze_missing_field():
    """Missing text field should return 422."""
    response = client.post("/analyze", json={})
    assert response.status_code == 422
