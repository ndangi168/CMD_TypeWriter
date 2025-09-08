from typing import Optional

from .stats import StatsTracker
from ..data.models import RealtimeStats, TestResult


BACKSPACE = "\x7f"  # POSIX backspace
ENTER = "\n"

class TypingEngine:
    def __init__(self, text: str) -> None:
        self.text = text
        self.stats_tracker = StatsTracker(target_text=text, stats=RealtimeStats())
        self._started = False
        self._completed = False
        self._result: Optional[TestResult] = None
        self._buffer: str = ""

    def start_test(self) -> None:
        if self._started:
            return
        self._started = True
        self.stats_tracker.start()

    def process_keystroke(self, key: str) -> None:
        if self._completed:
            return
        if key == BACKSPACE:
            self._buffer = self._buffer[:-1]
        elif key == ENTER:
            # Allow newline as a space for our flat text
            self._buffer += " "
        else:
            self._buffer += key
        self.stats_tracker.update_from_input(self._buffer)

    def update_from_input_snapshot(self, user_input: str) -> None:
        self._buffer = user_input
        self.stats_tracker.update_from_input(self._buffer)

    def get_current_stats(self) -> RealtimeStats:
        return self.stats_tracker.stats

    def get_buffer(self) -> str:
        return self._buffer

    def is_complete(self) -> bool:
        return self._completed

    def finalize_test(self) -> TestResult:
        if not self._completed:
            self._completed = True
            self._result = self.stats_tracker.finalize()
        return self._result  # type: ignore[return-value]