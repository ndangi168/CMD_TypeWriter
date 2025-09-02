import time
import os
import sys
import random
import threading
from datetime import datetime

class Typewriter:
    def __init__(self):
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
        print(banner)

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