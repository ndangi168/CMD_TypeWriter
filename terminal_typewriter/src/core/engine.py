from typing import Optional

from .stats import StatsTracker
from ..data.models import RealtimeStats, TestResult


class TypingEngine:
    def __init__(self, text: str) -> None:
        self.text = text
        self.stats_tracker = StatsTracker(target_text=text, stats=RealtimeStats())
        self._started = False
        self._completed = False
        self._result: Optional[TestResult] = None

    def start_test(self) -> None:
        if self._started:
            return
        self._started = True
        self.stats_tracker.start()

    def process_keystroke(self, key: str) -> None:
        # Placeholder for future per-keystroke processing
        pass

    def update_from_input_snapshot(self, user_input: str) -> None:
        self.stats_tracker.update_from_input(user_input)

    def get_current_stats(self) -> RealtimeStats:
        return self.stats_tracker.stats

    def is_complete(self) -> bool:
        return self._completed

    def finalize_test(self) -> TestResult:
        if not self._completed:
            self._completed = True
            self._result = self.stats_tracker.finalize()
        return self._result  # type: ignore[return-value]