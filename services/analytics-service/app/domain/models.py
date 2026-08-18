from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CompletedSession:
    topic: str
    started_at: datetime
    completed_at: datetime
