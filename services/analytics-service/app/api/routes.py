from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.schemas import AnalyticsSummaryResponse
from app.auth.dependencies import AuthenticatedUser, get_authenticated_user
from app.clients.focus import FocusServiceClientError
from app.services.summary import InvalidTimezoneError, calculate_summary


router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/summary", response_model=AnalyticsSummaryResponse)
def analytics_summary(
    timezone_name: str = Query(alias="timezone", min_length=1),
    user: AuthenticatedUser = Depends(get_authenticated_user),
) -> AnalyticsSummaryResponse:
    try:
        return AnalyticsSummaryResponse.model_validate(
            calculate_summary(
                user_id=user.user_id,
                access_token=user.access_token,
                timezone_name=timezone_name,
            )
        )
    except InvalidTimezoneError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error
    except FocusServiceClientError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Focus Service request failed.",
        ) from error
