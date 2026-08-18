from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.models import SessionStatus


class CreateSessionRequest(BaseModel):
    topic: str = Field(min_length=1)
    planned_duration: int = Field(ge=0)


class SessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: str
    topic: str
    planned_duration: int
    started_at: datetime | None
    completed_at: datetime | None
    status: SessionStatus
    created_at: datetime
