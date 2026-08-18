from collections import Counter
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from app.clients.focus import get_completed_sessions
from app.domain.models import CompletedSession


class InvalidTimezoneError(ValueError):
    pass


def calculate_summary(
    *,
    user_id: str,
    access_token: str,
    timezone_name: str,
    now: datetime | None = None,
) -> dict[str, int | str | None]:
    try:
        zone = ZoneInfo(timezone_name)
    except (ZoneInfoNotFoundError, ValueError) as error:
        raise InvalidTimezoneError("timezone must be a valid IANA timezone.") from error

    current = (now or datetime.now(timezone.utc)).astimezone(zone)
    today = current.date()
    week_start = today - timedelta(days=today.weekday())
    today_start = _utc_boundary(today, zone)
    tomorrow_start = _utc_boundary(today + timedelta(days=1), zone)
    week_boundary = _utc_boundary(week_start, zone)
    next_week_boundary = _utc_boundary(week_start + timedelta(days=7), zone)

    sessions = get_completed_sessions(
        access_token=access_token,
        user_id=user_id,
        from_utc=week_boundary,
        to_utc=next_week_boundary,
    )
    today_sessions = [
        session
        for session in sessions
        if today_start <= session.completed_at < tomorrow_start
    ]
    return {
        "today_focus_seconds": _total_focus_seconds(today_sessions),
        "today_completed_sessions": len(today_sessions),
        "week_focus_seconds": _total_focus_seconds(sessions),
        "week_completed_sessions": len(sessions),
        "top_topic": _top_topic(sessions),
    }


def _utc_boundary(day: date, zone: ZoneInfo) -> datetime:
    return datetime.combine(day, time.min, tzinfo=zone).astimezone(timezone.utc)


def _total_focus_seconds(sessions: list[CompletedSession]) -> int:
    return sum(max(0, int((s.completed_at - s.started_at).total_seconds())) for s in sessions)


def _top_topic(sessions: list[CompletedSession]) -> str | None:
    if not sessions:
        return None
    counts = Counter(session.topic for session in sessions)
    return min(counts, key=lambda topic: (-counts[topic], topic))
