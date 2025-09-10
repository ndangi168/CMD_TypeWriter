from typing import Literal

MenuChoice = Literal["start", "history", "replay_last", "exit"]


class MenuSystem:
    def prompt(self) -> MenuChoice:
        print("\nMain Menu:")
        print("1. Start Typing Test")
        print("2. View Session History")
        print("3. Replay Last Session")
        print("4. Exit")
        while True:
            choice = input("Enter your choice (1-4): ").strip()
            if choice == '1':
                return "start"
            if choice == '2':
                return "history"
            if choice == '3':
                return "replay_last"
            if choice == '4':
                return "exit"
            print("Invalid choice. Please select 1, 2, 3, or 4.")