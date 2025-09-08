import sys
import termios
import tty
import select
from typing import Optional


class InputHandler:
    def __init__(self) -> None:
        self._orig_settings: Optional[list[int]] = None

    def __enter__(self):
        self._orig_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        return self

    def __exit__(self, exc_type, exc, tb):
        if self._orig_settings is not None:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self._orig_settings)

    def read_key(self) -> Optional[str]:
        dr, _, _ = select.select([sys.stdin], [], [], 0.01)
        if dr:
            ch = sys.stdin.read(1)
            return ch
        return None