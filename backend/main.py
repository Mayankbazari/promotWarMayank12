"""AI Emergency Decision Agent — FastAPI Application.

Multi-agent orchestrator that classifies emergencies and dispatches
specialized agents (medical, accident) to generate structured action plans.
"""

from __future__ import annotations

import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from agents.classifier import classify_emergency
from agents.planner import plan_response
from agents.medical import handle_medical
from agents.accident import handle_accident
from config import get_settings
from models.schemas import (
    AgentAction,
    EmergencyInput,
    EmergencyResponse,
)
from tools.emergency_tools import get_emergency_numbers, get_severity_actions

# ──────────────────────── Logging ────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


# ──────────────────────── Lifespan ────────────────────────


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown hooks."""
    settings = get_settings()
    if not settings.GEMINI_API_KEY:
        logger.warning("⚠️  GEMINI_API_KEY not set — agent calls will fail")
    else:
        logger.info("✅ Gemini API key configured (model: %s)", settings.GEMINI_MODEL)
    yield
    logger.info("🛑 Shutting down Emergency Decision Agent")


# ──────────────────────── App ────────────────────────

app = FastAPI(
    title="AI Emergency Decision Agent",
    description=(
        "Multi-agent system that classifies emergencies and generates "
        "structured action plans using Google Gemini."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ──────────────────────── Routes ────────────────────────


@app.get("/")
def read_root():
    """Redirect to docs or show welcome message."""
    return {
        "message": "Welcome to AI Emergency Decision Agent API",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
def health_check():
    """Health check endpoint for Cloud Run."""
    return {"status": "healthy", "service": "emergency-decision-agent"}


@app.post("/analyze", response_model=EmergencyResponse)
def analyze_emergency(data: EmergencyInput):
    """Orchestrate the multi-agent emergency analysis pipeline.

    Flow:
        1. Classifier Agent → categorize emergency type & severity
        2. Planner Agent → decide which specialized agents to invoke
        3. Specialized Agents → generate actionable guidance
        4. Tools → attach emergency numbers & severity rules
    """
    start = time.time()
    logger.info("📨 Received emergency: %s", data.text[:100])

    try:
        # Step 1: Classify
        classification = classify_emergency(data.text)
        logger.info(
            "🏷️  Classification: type=%s severity=%s confidence=%.2f",
            classification.type.value,
            classification.severity.value,
            classification.confidence,
        )

        # Step 2: Plan
        plan = plan_response(classification)
        logger.info("📋 Plan: agents=%s", plan.agents)

        # Step 3: Dispatch specialized agents
        actions: list[AgentAction] = []

        if "medical_agent" in plan.agents:
            medical_result = handle_medical(data.text)
            actions.append(
                AgentAction(agent_name="medical_agent", result=medical_result)
            )
            logger.info("🏥 Medical agent: condition=%s", medical_result.condition)

        if "accident_agent" in plan.agents:
            accident_result = handle_accident(data.text)
            actions.append(
                AgentAction(agent_name="accident_agent", result=accident_result)
            )
            logger.info("🚨 Accident agent: risk=%s", accident_result.risk.value)

        # Step 4: Attach tools
        emergency_numbers = get_emergency_numbers()
        severity_actions = get_severity_actions(classification.severity)

        # Build summary
        summary = (
            f"Emergency classified as {classification.type.value} "
            f"({classification.severity.value} severity). "
            f"Priority guidance: {severity_actions[0]}"
        )

        elapsed = time.time() - start
        logger.info("✅ Analysis complete in %.2fs", elapsed)

        return EmergencyResponse(
            classification=classification,
            plan=plan,
            actions=actions,
            emergency_numbers=emergency_numbers,
            summary=summary,
        )

    except RuntimeError as exc:
        logger.error("❌ Agent pipeline failed: %s", exc)
        raise HTTPException(
            status_code=502,
            detail=f"AI agent pipeline error: {exc}",
        ) from exc
    except Exception as exc:
        logger.error("❌ Unexpected error: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Internal server error while processing emergency",
        ) from exc
