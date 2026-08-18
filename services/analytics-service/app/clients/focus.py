from datetime import datetime

import httpx

from app.config import get_focus_internal_api_key, get_focus_service_url
from app.domain.models import CompletedSession


class FocusServiceClientError(RuntimeError):
    pass


def get_completed_sessions(
    *,
    access_token: str,
    user_id: str,
    from_utc: datetime,
    to_utc: datetime,
) -> list[CompletedSession]:
    del user_id
    try:
        response = httpx.get(
            f"{get_focus_service_url()}/internal/sessions/completed",
            headers={
                "Authorization": f"Bearer {access_token}",
                "X-Internal-API-Key": get_focus_internal_api_key(),
            },
            params={"from_utc": from_utc.isoformat(), "to_utc": to_utc.isoformat()},
            timeout=5.0,
        )
        response.raise_for_status()
        payload = response.json()
    except (httpx.HTTPError, ValueError) as error:
        raise FocusServiceClientError("Focus Service request failed.") from error

    return [
        CompletedSession(
            topic=item["topic"],
            started_at=datetime.fromisoformat(item["started_at"]),
            completed_at=datetime.fromisoformat(item["completed_at"]),
        )
        for item in payload
    ]
