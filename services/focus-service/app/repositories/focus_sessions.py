from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import FocusSessionRecord, SessionStatus


class FocusSessionRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def create(self, session: FocusSessionRecord) -> FocusSessionRecord:
        self._db.add(session)
        self._db.commit()
        self._db.refresh(session)
        return session

    def get_by_id_for_user(
        self,
        session_id: UUID,
        user_id: str,
    ) -> FocusSessionRecord | None:
        statement = select(FocusSessionRecord).where(
            FocusSessionRecord.id == session_id,
            FocusSessionRecord.user_id == user_id,
        )
        return self._db.scalar(statement)

    def get_running_by_user(self, user_id: str) -> FocusSessionRecord | None:
        statement = select(FocusSessionRecord).where(
            FocusSessionRecord.user_id == user_id,
            FocusSessionRecord.status == SessionStatus.RUNNING,
        )
        return self._db.scalar(statement)

    def list_by_user(self, user_id: str) -> list[FocusSessionRecord]:
        statement = (
            select(FocusSessionRecord)
            .where(FocusSessionRecord.user_id == user_id)
            .order_by(FocusSessionRecord.created_at.desc())
        )
        return list(self._db.scalars(statement))

    def list_completed_by_user(
        self,
        user_id: str,
        *,
        from_utc: datetime | None = None,
        to_utc: datetime | None = None,
    ) -> list[FocusSessionRecord]:
        statement = select(FocusSessionRecord).where(
            FocusSessionRecord.user_id == user_id,
            FocusSessionRecord.status == SessionStatus.COMPLETED,
        )
        if from_utc is not None:
            statement = statement.where(FocusSessionRecord.completed_at >= from_utc)
        if to_utc is not None:
            statement = statement.where(FocusSessionRecord.completed_at < to_utc)
        statement = statement.order_by(FocusSessionRecord.completed_at.asc())
        return list(self._db.scalars(statement))

    def save(self, session: FocusSessionRecord) -> FocusSessionRecord:
        self._db.commit()
        self._db.refresh(session)
        return session
