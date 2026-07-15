"""Transparent risk analysis for security events."""

from dataclasses import asdict, dataclass
from typing import Literal


RiskLevel = Literal["low", "guarded", "elevated", "high", "critical"]

SEVERITY_SCORES = {
    "info": 10,
    "low": 25,
    "medium": 50,
    "high": 75,
    "critical": 95,
}

EVENT_BONUSES = {
    "door_opened": 2,
    "motion_detected": 5,
    "temperature_alert": 6,
    "person_detected": 8,
    "forced_entry": 15,
    "weapon_detected": 20,
}


@dataclass(frozen=True)
class RiskAssessment:
    """Explainable risk result for one security event."""

    score: int
    level: RiskLevel
    reasons: list[str]

    def to_dict(self) -> dict:
        """Convert the assessment into an API-ready dictionary."""
        return asdict(self)


def determine_risk_level(score: int) -> RiskLevel:
    """Convert a numeric risk score into a readable level."""
    if score >= 85:
        return "critical"
    if score >= 70:
        return "high"
    if score >= 50:
        return "elevated"
    if score >= 30:
        return "guarded"
    return "low"


def analyze_event(
    severity: str,
    event_type: str,
    confidence: float | None,
) -> RiskAssessment:
    """Calculate an explainable risk score from event information."""
    severity_score = SEVERITY_SCORES.get(severity, SEVERITY_SCORES["info"])
    normalized_confidence = 0.50 if confidence is None else confidence
    normalized_confidence = max(0.0, min(normalized_confidence, 1.0))
    event_bonus = EVENT_BONUSES.get(event_type, 0)

    score = round(
        (severity_score * 0.70)
        + (normalized_confidence * 100 * 0.30)
        + event_bonus
    )
    score = min(score, 100)

    reasons = [
        f"Severity classified as {severity}.",
        f"Detection confidence is {normalized_confidence:.0%}.",
    ]

    if event_bonus:
        reasons.append(
            f"Event type {event_type} adds {event_bonus} risk points."
        )

    return RiskAssessment(
        score=score,
        level=determine_risk_level(score),
        reasons=reasons,
    )