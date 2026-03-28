"""Emergency tools — deterministic utilities used by agents."""

from __future__ import annotations

from models.schemas import EmergencyNumbers, SeverityLevel


def get_emergency_numbers() -> EmergencyNumbers:
    """Return standard Indian emergency contact numbers."""
    return EmergencyNumbers(
        ambulance="108",
        police="100",
        fire="101",
    )


# Severity escalation rules
SEVERITY_RULES: dict[str, list[str]] = {
    "critical": [
        "Call emergency services IMMEDIATELY",
        "Do NOT delay — every second counts",
        "Stay on the line with the dispatcher",
    ],
    "high": [
        "Call emergency services as soon as possible",
        "Monitor the situation closely",
        "Prepare to provide first aid if trained",
    ],
    "medium": [
        "Assess the situation carefully",
        "Call emergency services if condition worsens",
        "Keep the person comfortable",
    ],
    "low": [
        "Monitor the situation",
        "Seek medical attention when convenient",
        "Apply basic first aid if needed",
    ],
}


def get_severity_actions(severity: SeverityLevel) -> list[str]:
    """Return severity-specific action guidelines."""
    return SEVERITY_RULES.get(severity.value, SEVERITY_RULES["medium"])
