from typing import Literal

MenuChoice = Literal["start", "history", "replay_last", "start_curses", "analytics", "achievements", "settings", "exit"]


class MenuSystem:
    def prompt(self) -> MenuChoice:
        print("\nMain Menu:")
        print("1. Start Typing Test")
        print("2. View Session History")
        print("3. Replay Last Session")
        print("4. Start Typing Test (curses)")
        print("5. Analytics & Progress")
        print("6. Achievements")
        print("7. Settings")
        print("8. Exit")
        while True:
            choice = input("Enter your choice (1-8): ").strip()
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
                return "achievements"
            if choice == '7':
                return "settings"
            if choice == '8':
                return "exit"
            print("Invalid choice. Please select 1, 2, 3, 4, 5, 6, 7, or 8.")