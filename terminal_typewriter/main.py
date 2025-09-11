import sys
import time
from typing import Optional

from src.core.text_manager import TextManager
from src.core.engine import TypingEngine
from src.core.timer import CountdownTimer
from src.ui.display import DisplayManager
from src.ui.menu import MenuSystem
from src.ui.input_handler import InputHandler
from src.ui.curses_display import CursesDisplay
from src.data.storage import StorageManager
from src.utils.helpers import generate_session_id, now_utc_iso
from src.features.reports import format_history_table
from src.features.replay import ReplaySystem


def prompt_level() -> str:
    print("\n Select Difficulty Level:")
    print("1. Beginner   - Simple words and common phrases")
    print("2. Intermediate - Mixed sentences with punctuation")
    print("3. Advanced   - Complex text with numbers and symbols")
    print("4. Expert     - Programming code snippets")
    levels = {
        '1': 'beginner',
        '2': 'intermediate',
        '3': 'advanced',
        '4': 'expert',
    }
    while True:
        choice = input("Enter your choice (1-4): ").strip()
        if choice in levels:
            return levels[choice]
        print("Invalid choice. Please select a number between 1 and 4.")


def prompt_duration() -> int:
    print("\n Set Time Duration for Typing Test:")
    print("1. 30 seconds")
    print("2. 1 minute")
    print("3. 2 minutes")
    print("4. Custom (enter seconds)")
    while True:
        choice = input("Enter your choice (1-4): ").strip()
        if choice == '1':
            return 30
        if choice == '2':
            return 60
        if choice == '3':
            return 120
        if choice == '4':
            custom = input("Enter custom time in seconds (e.g., 45): ").strip()
            if custom.isdigit() and int(custom) > 0:
                return int(custom)
            print("Please enter a valid positive integer for seconds.")
            continue
        print("Invalid choice. Please select a number between 1 and 4.")


def run_test_flow(display: DisplayManager, text_manager: TextManager, storage: StorageManager) -> None:
    level = prompt_level()
    duration = prompt_duration()
    text = text_manager.get_text(level, duration)

    display.clear()
    display.banner()
    display.show_text(level, duration, text)
    input("Press Enter when you're ready to start...")

    engine = TypingEngine(text)
    engine.start_test()

    timer = CountdownTimer(
        duration_seconds=duration,
        on_tick=lambda r: None,
        on_complete=lambda: None,
    )
    timer.start()

    last_render = 0.0
    render_interval = 0.1

    display.clear()
    display.banner()
    print(text)

    with InputHandler() as ih:
        while timer.remaining > 0:
            key = ih.read_key()
            if key is not None:
                engine.process_keystroke(key)
            now = time.time()
            if now - last_render >= render_interval:
                last_render = now
                display.render_live(engine, timer.remaining)

    result = engine.finalize_test()

    session_id = generate_session_id()
    storage.save_session({
        "id": session_id,
        "timestamp": now_utc_iso(),
        "mode": level,
        "duration": result.duration_seconds,
        "text_length": result.text_length,
        "wpm": result.wpm,
        "accuracy": result.accuracy,
        "errors": result.errors,
        "keystrokes": engine.get_keystrokes(),
        "text": text,
    })

    display.clear()
    display.banner()
    display.show_results(result)


def run_test_flow_curses(text_manager: TextManager, storage: StorageManager) -> None:
    level = prompt_level()
    duration = prompt_duration()
    text = text_manager.get_text(level, duration)

    def _session(stdscr):
        engine = TypingEngine(text)
        ui = CursesDisplay(stdscr)
        ui.run_session(text=text, duration=duration, engine=engine)
        result = engine.finalize_test()
        session_id = generate_session_id()
        storage.save_session({
            "id": session_id,
            "timestamp": now_utc_iso(),
            "mode": level,
            "duration": result.duration_seconds,
            "text_length": result.text_length,
            "wpm": result.wpm,
            "accuracy": result.accuracy,
            "errors": result.errors,
            "keystrokes": engine.get_keystrokes(),
            "text": text,
        })

    try:
        import curses
        curses.wrapper(_session)
    except Exception as exc:
        print("Curses mode failed, falling back to standard mode. Reason:", exc)
        display = DisplayManager()
        run_test_flow(display, text_manager, storage)


def view_history_flow(display: DisplayManager, storage: StorageManager) -> None:
    display.clear()
    display.banner()
    rows = storage.fetch_recent_sessions(limit=15)
    print("\nRecent Sessions:\n")
    print(format_history_table(rows))
    print("\nPress Enter to return to menu...")
    input()


def replay_last_flow(display: DisplayManager, storage: StorageManager, text_manager: TextManager) -> None:
    session = storage.fetch_latest_session_with_keystrokes()
    if not session:
        display.clear()
        display.banner()
        print("\nNo sessions available to replay.")
        print("\nPress Enter to return to menu...")
        input()
        return
    text = session.get("text") or ""

    display.clear()
    display.banner()
    print("Replaying last session... Press Ctrl+C to stop.\n")
    print(text)

    def on_frame(engine: TypingEngine):
        stats = engine.get_current_stats()
        print(f"\rWPM: {stats.wpm:>5}  Acc: {stats.accuracy:>5}%  Chars: {stats.characters_typed}", end="", flush=True)

    try:
        replayer = ReplaySystem(text=text, keystrokes=session.get("keystrokes", []))
        replayer.run(speed=1.0, on_frame=on_frame)
    except KeyboardInterrupt:
        pass
    finally:
        print("\n\nReplay finished. Press Enter to return to menu...")
        input()


def main() -> None:
    display = DisplayManager()
    text_manager = TextManager()
    storage = StorageManager()
    menu = MenuSystem()

    display.clear()
    display.banner()

    name = input("Enter your name: ")
    print(f"\nHello, {name}! Test your typing speed in terminal\n")

    while True:
        choice = menu.prompt()
        if choice == "start":
            run_test_flow(display, text_manager, storage)
        elif choice == "history":
            view_history_flow(display, storage)
        elif choice == "replay_last":
            replay_last_flow(display, storage, text_manager)
        elif choice == "start_curses":
            run_test_flow_curses(text_manager, storage)
        else:
            break

    print("\n\nThank you for using Terminal Typewriter. Goodbye!")


if __name__ == "__main__":
    main()
