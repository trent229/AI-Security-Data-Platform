"""Data models for security events."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


SeverityLevel = Literal["info", "low", "medium", "high", "critical"]


class SecurityEventCreate(BaseModel):
    """Information submitted by a security device."""

    device_id: str = Field(min_length=1, max_length=100)
    event_type: str = Field(min_length=1, max_length=100)
    severity: SeverityLevel = "info"
    description: str = Field(min_length=1, max_length=500)
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)


class SecurityEvent(SecurityEventCreate):
    """A complete event stored in the database."""

    id: int
    created_at: datetime