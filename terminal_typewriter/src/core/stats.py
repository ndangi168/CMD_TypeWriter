import time
from dataclasses import dataclass
from typing import Optional

from ..data.models import RealtimeStats, TestResult


CHARACTERS_PER_WORD = 5.0


@dataclass
class StatsTracker:
    target_text: str
    stats: RealtimeStats

    def start(self) -> None:
        self.stats.start_time = time.time()
        self.stats.elapsed_seconds = 0.0
        self.stats.characters_typed = 0
        self.stats.correct_characters = 0
        self.stats.errors = 0
        self.stats.wpm = 0.0
        self.stats.accuracy = 0.0

    def update_from_input(self, user_input: str) -> None:
        now = time.time()
        if self.stats.start_time is None:
            self.stats.start_time = now
        self.stats.elapsed_seconds = max(0.0, now - self.stats.start_time)

        typed_chars = len(user_input)
        original_chars = len(self.target_text)
        correct = 0
        for i in range(min(typed_chars, original_chars)):
            if user_input[i] == self.target_text[i]:
                correct += 1

        self.stats.characters_typed = typed_chars
        self.stats.correct_characters = correct
        self.stats.errors = max(0, typed_chars - correct)

        minutes = self.stats.elapsed_seconds / 60.0 if self.stats.elapsed_seconds > 0 else 0
        gross_wpm = (typed_chars / CHARACTERS_PER_WORD) / minutes if minutes > 0 else 0.0
        accuracy = (correct / original_chars * 100.0) if original_chars > 0 else 0.0

        self.stats.wpm = round(gross_wpm, 2)
        self.stats.accuracy = round(accuracy, 2)

    def finalize(self) -> TestResult:
        duration = self.stats.elapsed_seconds
        result = TestResult(
            duration_seconds=round(duration, 2),
            text_length=len(self.target_text),
            wpm=self.stats.wpm,
            accuracy=self.stats.accuracy,
            errors=self.stats.errors,
        )
        return result