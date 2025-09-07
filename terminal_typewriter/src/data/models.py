from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class RealtimeStats:
    start_time: Optional[float] = None
    elapsed_seconds: float = 0.0
    characters_typed: int = 0
    correct_characters: int = 0
    errors: int = 0
    wpm: float = 0.0
    accuracy: float = 0.0


@dataclass
class TestResult:
    duration_seconds: float
    text_length: int
    wpm: float
    accuracy: float
    errors: int


@dataclass
class TypingSession:
    id: str
    timestamp: datetime
    mode: str
    duration: float
    text: str
    keystrokes: List[Dict[str, Any]] = field(default_factory=list)
    result: Optional[TestResult] = None


@dataclass
class UserSettings:
    name: str = "Guest"
    difficulty: str = "beginner"
    duration_seconds: int = 60
    theme: str = "default"