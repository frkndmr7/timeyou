from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.db.models import FocusSessionRecord, SessionStatus
from app.repositories.focus_sessions import FocusSessionRepository


class SessionNotFoundError(LookupError):
    pass


class SessionStateError(ValueError):
    pass


class RunningSessionExistsError(ValueError):
    pass


def start_session(session: FocusSessionRecord) -> FocusSessionRecord:
    if session.status is not SessionStatus.PENDING:
        raise SessionStateError("Only pending sessions can be started.")
    if session.started_at is not None:
        raise SessionStateError("Session has already started.")

    session.status = SessionStatus.RUNNING
    session.started_at = datetime.now(timezone.utc)
    return session


def complete_session(session: FocusSessionRecord) -> FocusSessionRecord:
    if session.status is not SessionStatus.RUNNING:
        raise SessionStateError("Only running sessions can be completed.")
    if session.started_at is None:
        raise SessionStateError("A session must be started before completion.")

    session.status = SessionStatus.COMPLETED
    session.completed_at = datetime.now(timezone.utc)
    return session


def cancel_session(session: FocusSessionRecord) -> FocusSessionRecord:
    if session.status not in {SessionStatus.PENDING, SessionStatus.RUNNING}:
        raise SessionStateError("Only pending or running sessions can be cancelled.")

    session.status = SessionStatus.CANCELLED
    session.completed_at = None
    return session


class FocusSessionService:
    def __init__(self, repository: FocusSessionRepository) -> None:
        self._repository = repository

    def create(
        self,
        *,
        user_id: str,
        topic: str,
        planned_duration: int,
    ) -> FocusSessionRecord:
        if self._repository.get_running_by_user(user_id) is not None:
            raise RunningSessionExistsError(
                "User already has a running session."
            )

        session = FocusSessionRecord(
            id=uuid4(),
            user_id=user_id,
            topic=topic,
            planned_duration=planned_duration,
            status=SessionStatus.PENDING,
        )
        return self._repository.create(session)

    def start(self, session_id: UUID, user_id: str) -> FocusSessionRecord:
        session = self._get(session_id, user_id)
        return self._repository.save(start_session(session))

    def complete(self, session_id: UUID, user_id: str) -> FocusSessionRecord:
        session = self._get(session_id, user_id)
        return self._repository.save(complete_session(session))

    def cancel(self, session_id: UUID, user_id: str) -> FocusSessionRecord:
        session = self._get(session_id, user_id)
        return self._repository.save(cancel_session(session))

    def list(self, user_id: str) -> list[FocusSessionRecord]:
        return self._repository.list_by_user(user_id)

    def list_completed(
        self,
        user_id: str,
        *,
        from_utc: datetime | None = None,
        to_utc: datetime | None = None,
    ) -> list[FocusSessionRecord]:
        return self._repository.list_completed_by_user(
            user_id,
            from_utc=from_utc,
            to_utc=to_utc,
        )

    def _get(self, session_id: UUID, user_id: str) -> FocusSessionRecord:
        session = self._repository.get_by_id_for_user(session_id, user_id)
        if session is None:
            raise SessionNotFoundError(f"Session {session_id} was not found.")
        return session
