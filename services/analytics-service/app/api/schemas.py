from pydantic import BaseModel, Field


class AnalyticsSummaryResponse(BaseModel):
    today_focus_seconds: int = Field(ge=0)
    today_completed_sessions: int = Field(ge=0)
    week_focus_seconds: int = Field(ge=0)
    week_completed_sessions: int = Field(ge=0)
    top_topic: str | None
