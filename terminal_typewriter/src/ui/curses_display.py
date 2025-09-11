import time
from typing import Tuple

import curses

from ..core.engine import TypingEngine, BACKSPACE, ENTER


class CursesDisplay:
    def __init__(self, stdscr) -> None:
        self.stdscr = stdscr
        curses.curs_set(1)
        self.stdscr.nodelay(True)
        self.stdscr.keypad(True)

    def _draw_layout(self, remaining: int, engine: TypingEngine, text: str) -> None:
        self.stdscr.erase()
        max_y, max_x = self.stdscr.getmaxyx()

        # Header
        stats = engine.get_current_stats()
        header = f"⏳ {remaining:>3}s  |  WPM: {stats.wpm:>5}  |  Acc: {stats.accuracy:>5}%  |  Chars: {stats.characters_typed}"
        self.stdscr.addnstr(0, 0, header.ljust(max_x), max_x)
        self.stdscr.hline(1, 0, curses.ACS_HLINE, max_x)

        # Text area
        text_lines = []
        line = []
        for word in text.split(" "):
            if sum(len(w) for w in line) + max(0, len(line) - 1) + len(word) + 1 > max_x:
                text_lines.append(" ".join(line))
                line = [word]
            else:
                line.append(word)
        if line:
            text_lines.append(" ".join(line))
        for idx, tline in enumerate(text_lines[: max(1, max_y - 6)]):
            self.stdscr.addnstr(2 + idx, 0, tline, max_x)

        # Separator
        self.stdscr.hline(max_y - 4, 0, curses.ACS_HLINE, max_x)

        # Input label
        self.stdscr.addnstr(max_y - 3, 0, "Your input:", max_x)

        # Input echo (last lines)
        buf = engine.get_buffer()
        view_height = 2
        view_width = max_x - 1
        lines = []
        current = ""
        for ch in buf:
            if ch == "\n":
                lines.append(current)
                current = ""
            else:
                if len(current) >= view_width:
                    lines.append(current)
                    current = ch
                else:
                    current += ch
        lines.append(current)
        start_line = max(0, len(lines) - view_height)
        for i in range(view_height):
            content = lines[start_line + i] if start_line + i < len(lines) else ""
            self.stdscr.addnstr(max_y - 2 + i, 0, content.ljust(view_width), view_width)

        # Place caret
        caret_y = max_y - 2 + min(view_height - 1, len(lines) - 1 - start_line)
        caret_x = min(len(lines[-1]), view_width - 1)
        try:
            self.stdscr.move(caret_y, caret_x)
        except curses.error:
            pass

        self.stdscr.refresh()

    def run_session(self, text: str, duration: int, engine: TypingEngine) -> None:
        engine.start_test()
        start = time.time()
        remaining = duration
        while remaining > 0:
            # Input handling
            try:
                key = self.stdscr.getch()
            except curses.error:
                key = -1
            if key != -1:
                if key in (curses.KEY_BACKSPACE, 127):
                    engine.process_keystroke(BACKSPACE)
                elif key in (10, 13):
                    engine.process_keystroke(ENTER)
                elif 0 <= key <= 255:
                    engine.process_keystroke(chr(key))
            # Render
            self._draw_layout(remaining, engine, text)
            # Update remaining
            elapsed = int(time.time() - start)
            remaining = max(0, duration - elapsed)
            time.sleep(0.02)