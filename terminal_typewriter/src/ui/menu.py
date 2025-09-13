from typing import Literal

MenuChoice = Literal["start", "history", "replay_last", "start_curses", "analytics", "settings", "exit"]


class MenuSystem:
    def prompt(self) -> MenuChoice:
        print("\nMain Menu:")
        print("1. Start Typing Test")
        print("2. View Session History")
        print("3. Replay Last Session")
        print("4. Start Typing Test (curses)")
        print("5. Analytics & Progress")
        print("6. Settings")
        print("7. Exit")
        while True:
            choice = input("Enter your choice (1-7): ").strip()
            if choice == '1':
                return "start"
            if choice == '2':
                return "history"
            if choice == '3':
                return "replay_last"
            if choice == '4':
                return "start_curses"
            if choice == '5':
                return "analytics"
            if choice == '6':
                return "settings"
            if choice == '7':
                return "exit"
            print("Invalid choice. Please select 1, 2, 3, 4, 5, 6, or 7.")