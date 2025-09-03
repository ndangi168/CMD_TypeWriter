import time
import os
import sys
import random
import threading
from datetime import datetime

class Typewriter:
    def __init__(self):
        self.selected_level = None
        self.selected_time = None
        pass

    def clear_screen(self):
        ''' Clear the terminal screen. posix for Linux/Mac, cls for Windows.'''
        os.system('clear' if os.name == 'posix' else 'cls')

    def type_text(self, text, delay=0.05):
        ''' Simulate typing effect by printing one character at a time with a delay.'''
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def display_banner(self):
        banner = r"""
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                          🎯 TERMINAL TYPEWRITER 🎯                           ║
    ║                        Calculate Your Typing Speed                           ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
        """
        self.type_text(banner, delay=0.002)
        #print(banner)

    def get_difficulty_level(self):
        """Get difficulty level selection from user"""
        print("\n Select Difficulty Level:")
        print("1. Beginner   - Simple words and common phrases")
        print("2. Intermediate - Mixed sentences with punctuation")
        print("3. Advanced   - Complex text with numbers and symbols")
        print("4. Expert     - Programming code snippets")

        while True:
            try:
                choice = input("Enter your choice (1-4): ")
                if choice.strip() == "":
                    print("Input cannot be empty. Please try again.")
                    continue
                if choice in ['1', '2', '3', '4']:
                    levels = {
                        '1': 'beginner',
                        '2': 'intermediate', 
                        '3': 'advanced',
                        '4': 'expert'
                    }
                    self.selected_level = levels[choice]
                    print(f"You selected {self.selected_level.capitalize()} level.")
                    return True
                else:
                    print("Invalid choice. Please select a number between 1 and 4.")
            except KeyboardInterrupt:
                print("\nProgram terminated by user.")
                sys.exit(0)
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Please try again.")
                sys.exit(0)

    def get_time(self):
        """Get time duration for typing test from user"""
        print("\n Set Time Duration for Typing Test:")
        print("1. 30 seconds")
        print("2. 1 minute")
        print("3. 2 minutes")
        print("4. Custom (enter seconds)")
        while True:
            try:
                choice = input("Enter your choice (1-4): ")
                if choice.strip() == "":
                    print("Input cannot be empty. Please try again.")
                    continue
                if choice in ['1', '2', '3', '4']:
                    if choice == '1':
                        self.selected_time = 30
                    elif choice == '2':
                        self.selected_time = 60
                    elif choice == '3':
                        self.selected_time = 120
                    elif choice == '4':
                        while True:
                            custom_time = input("Enter custom time in seconds (e.g., 45): ")
                            if custom_time.isdigit() and int(custom_time) > 0:
                                self.selected_time = int(custom_time)
                            else:
                                print("Please enter a valid positive integer for seconds.")
                else:
                    print("Invalid choice. Please select a number between 1 and 4.")
                    continue
                return True
            except KeyboardInterrupt:
                print("\nProgram terminated by user.")
                sys.exit(0)
            except Exception as e:
                print(f"An error occurred: {e}")
                print("Please try again.")
                sys.exit(0)

    def run(self):
        self.clear_screen()
        self.display_banner()
        name = input("Enter your name: ")
        sample_texts = [
            "The quick brown fox jumps over the lazy dog.",
            "Typing is a skill that improves with practice.",
            "Consistency is key to mastering any skill.",
            "Practice makes perfect, so keep typing!"
        ]
        text_to_type = random.choice(sample_texts)
        print(f"Hello, {name}! Type the following text as fast as you can:\n")
        print(text_to_type)
        input("\nPress Enter when you're ready to start...")
        print("Start typing now:\n")
        
        start_time = datetime.now()
        user_input = input()
        end_time = datetime.now()

        time_taken = (end_time - start_time).total_seconds()
        words_typed = len(user_input.split())
        wpm = (words_typed / time_taken) * 60 if time_taken > 0 else 0

        self.clear_screen()
        self.display_banner()
        print(f"Time taken: {time_taken:.2f} seconds")
        print(f"Words typed: {words_typed}")
        print(f"Your typing speed: {wpm:.2f} WPM")
        
        if user_input.strip() == text_to_type.strip():
            print("Great job! You typed the text correctly.")
        else:
            print("There were some mistakes in your typing. Keep practicing!")

def main():
    app = Typewriter()
    app.run()

if __name__ == "__main__":
    main()