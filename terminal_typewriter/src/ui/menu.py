from typing import Literal

MenuChoice = Literal["start", "history", "replay_last", "start_curses", "settings", "exit"]


class MenuSystem:
    def prompt(self) -> MenuChoice:
        print("\nMain Menu:")
        print("1. Start Typing Test")
        print("2. View Session History")
        print("3. Replay Last Session")
        print("4. Start Typing Test (curses)")
        print("5. Settings")
        print("6. Exit")
        while True:
            choice = input("Enter your choice (1-6): ").strip()
            if choice == '1':
                return "start"
            if choice == '2':
                return "history"
            if choice == '3':
                return "replay_last"
            if choice == '4':
                return "start_curses"
            if choice == '5':
                return "settings"
            if choice == '6':
                return "exit"
            print("Invalid choice. Please select 1, 2, 3, 4, 5, or 6.")