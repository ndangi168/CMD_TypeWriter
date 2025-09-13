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
from src.utils.config import ConfigManager
from src.features.reports import format_history_table
from src.features.replay import ReplaySystem
from src.features.analytics import Analytics


def prompt_level(config: ConfigManager) -> str:
    default_level = config.get("default_difficulty", "beginner")
    print(f"\n Select Difficulty Level (default: {default_level}):")
    print("1. Beginner   - Simple words and common phrases")
    print("2. Intermediate - Mixed sentences with punctuation")
    print("3. Advanced   - Complex text with numbers and symbols")
    print("4. Expert     - Programming code snippets")
    print("5. Use default")
    levels = {
        '1': 'beginner',
        '2': 'intermediate',
        '3': 'advanced',
        '4': 'expert',
        '5': default_level,
    }
    while True:
        choice = input("Enter your choice (1-5): ").strip()
        if choice in levels:
            return levels[choice]
        print("Invalid choice. Please select a number between 1 and 5.")


def prompt_duration(config: ConfigManager) -> int:
    default_duration = config.get("default_duration", 60)
    print(f"\n Set Time Duration for Typing Test (default: {default_duration}s):")
    print("1. 30 seconds")
    print("2. 1 minute")
    print("3. 2 minutes")
    print("4. Custom (enter seconds)")
    print("5. Use default")
    while True:
        choice = input("Enter your choice (1-5): ").strip()
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
        if choice == '5':
            return default_duration
        print("Invalid choice. Please select a number between 1 and 5.")


def run_test_flow(display: DisplayManager, text_manager: TextManager, storage: StorageManager, config: ConfigManager) -> None:
    level = prompt_level(config)
    duration = prompt_duration(config)
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


def run_test_flow_curses(text_manager: TextManager, storage: StorageManager, config: ConfigManager) -> None:
    level = prompt_level(config)
    duration = prompt_duration(config)
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
        run_test_flow(display, text_manager, storage, config)


def view_history_flow(display: DisplayManager, storage: StorageManager) -> None:
    display.clear()
    display.banner()
    rows = storage.fetch_recent_sessions(limit=15)
    print("\nRecent Sessions:\n")
    print(format_history_table(rows))
    print("\nPress Enter to return to menu...")
    input()


def analytics_flow(display: DisplayManager, storage: StorageManager) -> None:
    display.clear()
    display.banner()
    
    sessions = storage.fetch_recent_sessions(limit=100)  # Get more sessions for analytics
    analytics = Analytics(sessions)
    
    print("\n" + analytics.format_summary_report())
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


def settings_flow(display: DisplayManager, config: ConfigManager) -> None:
    display.clear()
    display.banner()
    
    print("\nSettings:")
    print("1. Change default difficulty")
    print("2. Change default duration")
    print("3. Change theme")
    print("4. Change user name")
    print("5. View current settings")
    print("6. Reset to defaults")
    print("7. Back to main menu")
    
    while True:
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == "1":
            print("\nCurrent default difficulty:", config.get("default_difficulty"))
            new_level = prompt_level(config)
            config.set("default_difficulty", new_level)
            print(f"Default difficulty set to: {new_level}")
            
        elif choice == "2":
            print("\nCurrent default duration:", config.get("default_duration"))
            new_duration = prompt_duration(config)
            config.set("default_duration", new_duration)
            print(f"Default duration set to: {new_duration} seconds")
            
        elif choice == "3":
            print("\nCurrent theme:", config.get("default_theme"))
            themes = config.list_themes()
            print("Available themes:")
            for i, (key, name) in enumerate(themes.items(), 1):
                print(f"{i}. {name} ({key})")
            try:
                theme_choice = input("Enter theme number: ").strip()
                theme_keys = list(themes.keys())
                if theme_choice.isdigit() and 1 <= int(theme_choice) <= len(theme_keys):
                    selected_theme = theme_keys[int(theme_choice) - 1]
                    config.set("default_theme", selected_theme)
                    print(f"Theme set to: {themes[selected_theme]}")
                else:
                    print("Invalid choice")
            except (ValueError, IndexError):
                print("Invalid choice")
                
        elif choice == "4":
            print("\nCurrent name:", config.get("user_name"))
            new_name = input("Enter new name: ").strip()
            if new_name:
                config.set("user_name", new_name)
                print(f"Name set to: {new_name}")
                
        elif choice == "5":
            print("\nCurrent Settings:")
            print(f"  Default difficulty: {config.get('default_difficulty')}")
            print(f"  Default duration: {config.get('default_duration')} seconds")
            print(f"  Theme: {config.get('default_theme')}")
            print(f"  User name: {config.get('user_name')}")
            print(f"  Auto save sessions: {config.get('auto_save_sessions')}")
            
        elif choice == "6":
            confirm = input("Reset all settings to defaults? (y/N): ").strip().lower()
            if confirm in ['y', 'yes']:
                config.reset_to_defaults()
                print("Settings reset to defaults")
                
        elif choice == "7":
            break
            
        else:
            print("Invalid choice")
    
    config.save_settings()


def main() -> None:
    display = DisplayManager()
    text_manager = TextManager()
    storage = StorageManager()
    config = ConfigManager()
    menu = MenuSystem()

    display.clear()
    display.banner()

    # Use config for name or prompt if not set
    name = config.get("user_name", "Guest")
    if name == "Guest":
        name = input("Enter your name: ")
        config.set("user_name", name)
        config.save_settings()
    
    print(f"\nHello, {name}! Test your typing speed in terminal\n")

    while True:
        choice = menu.prompt()
        if choice == "start":
            run_test_flow(display, text_manager, storage, config)
        elif choice == "history":
            view_history_flow(display, storage)
        elif choice == "replay_last":
            replay_last_flow(display, storage, text_manager)
        elif choice == "start_curses":
            run_test_flow_curses(text_manager, storage, config)
        elif choice == "analytics":
            analytics_flow(display, storage)
        elif choice == "settings":
            settings_flow(display, config)
        else:
            break

    print("\n\nThank you for using Terminal Typewriter. Goodbye!")


if __name__ == "__main__":
    main()
