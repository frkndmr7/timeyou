from datetime import datetime
from enum import StrEnum
from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, Index, Integer, String, Uuid, text
from sqlalchemy.dialects.postgresql import ENUM as PostgreSQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class SessionStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


session_status_enum = PostgreSQLEnum(
    SessionStatus,
    name="session_status",
    values_callable=lambda enum_type: [member.value for member in enum_type],
    create_type=False,
)


class FocusSessionRecord(Base):
    __tablename__ = "focus_sessions"
    __table_args__ = (
        CheckConstraint(
            "planned_duration >= 0",
            name="ck_focus_sessions_planned_duration_non_negative",
        ),
        Index(
            "uq_focus_sessions_one_running_per_user",
            "user_id",
            unique=True,
            postgresql_where=text("status = 'running'"),
        ),
    )

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True)
    user_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    topic: Mapped[str] = mapped_column(String, nullable=False)
    planned_duration: Mapped[int] = mapped_column(Integer, nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    status: Mapped[SessionStatus] = mapped_column(
        session_status_enum,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
