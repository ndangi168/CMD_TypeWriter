import sys
from typing import Optional

from src.core.text_manager import TextManager
from src.core.engine import TypingEngine
from src.ui.display import DisplayManager
from src.ui.menu import MenuSystem
from src.data.storage import StorageManager
from src.utils.helpers import generate_session_id, now_utc_iso
from src.features.reports import format_history_table


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
    try:
        user_input = input()
    except KeyboardInterrupt:
        user_input = ""
    engine.update_from_input_snapshot(user_input)
    result = engine.finalize_test()

    # Save session
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
        "keystrokes": [],
    })

    display.clear()
    display.banner()
    display.show_results(result)


def view_history_flow(display: DisplayManager, storage: StorageManager) -> None:
    display.clear()
    display.banner()
    rows = storage.fetch_recent_sessions(limit=15)
    print("\nRecent Sessions:\n")
    print(format_history_table(rows))
    print("\nPress Enter to return to menu...")
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
        else:
            break

    print("\n\nThank you for using Terminal Typewriter. Goodbye!")


if __name__ == "__main__":
    main()
