import threading
import time
from typing import Callable, Optional


class CountdownTimer:
    def __init__(self, duration_seconds: int, on_tick: Optional[Callable[[int], None]] = None, on_complete: Optional[Callable[[], None]] = None) -> None:
        self.duration_seconds = duration_seconds
        self.on_tick = on_tick
        self.on_complete = on_complete
        self._thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self.remaining = duration_seconds

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self) -> None:
        start = time.time()
        while not self._stop_event.is_set():
            elapsed = int(time.time() - start)
            self.remaining = max(0, self.duration_seconds - elapsed)
            if self.on_tick:
                self.on_tick(self.remaining)
            if self.remaining <= 0:
                if self.on_complete:
                    self.on_complete()
                break
            time.sleep(1)

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=0.2)