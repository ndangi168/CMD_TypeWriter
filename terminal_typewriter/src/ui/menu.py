from typing import Literal

MenuChoice = Literal["start", "history", "exit"]


class MenuSystem:
    def prompt(self) -> MenuChoice:
        print("\nMain Menu:")
        print("1. Start Typing Test")
        print("2. View Session History")
        print("3. Exit")
        while True:
            choice = input("Enter your choice (1-3): ").strip()
            if choice == '1':
                return "start"
            if choice == '2':
                return "history"
            if choice == '3':
                return "exit"
            print("Invalid choice. Please select 1, 2, or 3.")