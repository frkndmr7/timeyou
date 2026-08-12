from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SessionStatus(StrEnum):
    RUNNING = "running"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class FocusSession(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: UUID
    user_id: str = Field(min_length=1)
    topic: str = Field(min_length=1)
    planned_duration: int = Field(ge=0)
    started_at: datetime
    completed_at: datetime | None = None
    status: SessionStatus
    created_at: datetime
