from collections.abc import Callable
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.auth.dependencies import get_current_user_id
from app.api.schemas import CreateSessionRequest, SessionResponse
from app.repositories.focus_sessions import FocusSessionRepository
from app.services.focus_sessions import (
    FocusSessionService,
    RunningSessionExistsError,
    SessionNotFoundError,
    SessionStateError,
)
from app.db.models import FocusSessionRecord


router = APIRouter(prefix="/sessions", tags=["sessions"])


def get_service(db: Session = Depends(get_db)) -> FocusSessionService:
    return FocusSessionService(FocusSessionRepository(db))


@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(
    request: CreateSessionRequest,
    user_id: str = Depends(get_current_user_id),
    service: FocusSessionService = Depends(get_service),
) -> SessionResponse:
    try:
        session = service.create(
            user_id=user_id,
            topic=request.topic,
            planned_duration=request.planned_duration,
        )
        return SessionResponse.model_validate(session)
    except RunningSessionExistsError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    except IntegrityError as error:
        raise HTTPException(status_code=409, detail="Running session already exists.") from error


@router.post("/{session_id}/start", response_model=SessionResponse)
def start_session(
    session_id: UUID,
    user_id: str = Depends(get_current_user_id),
    service: FocusSessionService = Depends(get_service),
) -> SessionResponse:
    return _run_transition(lambda: service.start(session_id, user_id))


@router.post("/{session_id}/complete", response_model=SessionResponse)
def complete_session(
    session_id: UUID,
    user_id: str = Depends(get_current_user_id),
    service: FocusSessionService = Depends(get_service),
) -> SessionResponse:
    return _run_transition(lambda: service.complete(session_id, user_id))


@router.post("/{session_id}/cancel", response_model=SessionResponse)
def cancel_session(
    session_id: UUID,
    user_id: str = Depends(get_current_user_id),
    service: FocusSessionService = Depends(get_service),
) -> SessionResponse:
    return _run_transition(lambda: service.cancel(session_id, user_id))


@router.get("", response_model=list[SessionResponse])
def list_sessions(
    user_id: str = Depends(get_current_user_id),
    service: FocusSessionService = Depends(get_service),
) -> list[SessionResponse]:
    return [SessionResponse.model_validate(session) for session in service.list(user_id)]


def _run_transition(
    operation: Callable[[], FocusSessionRecord],
) -> SessionResponse:
    try:
        session = operation()
        return SessionResponse.model_validate(session)
    except SessionNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error
    except SessionStateError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
