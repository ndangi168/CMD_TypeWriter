from dataclasses import dataclass
from typing import Optional

from ..data.models import TypingSession, UserSettings, RealtimeStats


@dataclass
class AppState:
    current_session: Optional[TypingSession]
    user_settings: UserSettings
    stats: RealtimeStats


def create_default_state() -> AppState:
    return AppState(
        current_session=None,
        user_settings=UserSettings(),
        stats=RealtimeStats(),
    )