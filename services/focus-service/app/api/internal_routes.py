from datetime import datetime

from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.api.schemas import SessionResponse
from app.auth.dependencies import get_current_user_id
from app.config import get_internal_api_key
from app.repositories.focus_sessions import FocusSessionRepository
from app.services.focus_sessions import FocusSessionService


router = APIRouter(prefix="/internal", tags=["internal"])


def get_internal_key(
    provided_key: str | None = Header(default=None, alias="X-Internal-API-Key"),
) -> None:
    if provided_key != get_internal_api_key():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid internal API key.",
        )


def get_service(db: Session = Depends(get_db)) -> FocusSessionService:
    return FocusSessionService(FocusSessionRepository(db))


@router.get(
    "/sessions/completed",
    response_model=list[SessionResponse],
    dependencies=[Depends(get_internal_key)],
)
def list_completed_sessions(
    from_utc: datetime | None = None,
    to_utc: datetime | None = None,
    user_id: str = Depends(get_current_user_id),
    service: FocusSessionService = Depends(get_service),
) -> list[SessionResponse]:
    return [
        SessionResponse.model_validate(session)
        for session in service.list_completed(
            user_id,
            from_utc=from_utc,
            to_utc=to_utc,
        )
    ]
