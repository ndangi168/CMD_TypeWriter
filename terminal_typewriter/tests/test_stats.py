from src.core.stats import StatsTracker
from src.data.models import RealtimeStats


def test_wpm_and_accuracy_basic():
    text = "hello world"
    stats = RealtimeStats()
    tracker = StatsTracker(target_text=text, stats=stats)
    tracker.start()
    # Simulate 30 seconds elapsed by directly setting start_time
    assert stats.start_time is not None
    stats.start_time -= 30.0

    tracker.update_from_input("hello world")

    # 11 characters => 11/5 = 2.2 words in 0.5 minutes => 4.4 WPM
    assert tracker.stats.wpm == 4.4
    assert tracker.stats.accuracy == 100.0


def test_accuracy_with_errors():
    text = "abcdef"
    stats = RealtimeStats()
    tracker = StatsTracker(target_text=text, stats=stats)
    tracker.start()
    assert stats.start_time is not None
    stats.start_time -= 60.0

    tracker.update_from_input("abcxyz")

    # 6 typed, 3 correct => 50% accuracy
    assert tracker.stats.accuracy == 50.0