import time
from typing import List, Dict, Any

from ..core.engine import TypingEngine, BACKSPACE, ENTER


class ReplaySystem:
    def __init__(self, text: str, keystrokes: List[Dict[str, Any]]) -> None:
        self.text = text
        # Expect keystrokes as list of {t: seconds, k: key}
        self.keystrokes = sorted(keystrokes, key=lambda x: x.get("t", 0))
        self.engine = TypingEngine(text)

    def run(self, speed: float = 1.0, on_frame=None) -> None:
        if speed <= 0:
            speed = 1.0
        self.engine.start_test()
        start = time.time()
        idx = 0
        while idx < len(self.keystrokes):
            now = time.time()
            elapsed = (now - start) * speed
            # Process all keystrokes whose timestamp <= elapsed
            while idx < len(self.keystrokes) and self.keystrokes[idx].get("t", 0) <= elapsed:
                key = self.keystrokes[idx].get("k", "")
                self.engine.process_keystroke(key)
                idx += 1
            if on_frame:
                on_frame(self.engine)
            time.sleep(0.02)
        self.engine.finalize_test()