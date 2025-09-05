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
        self.current_text = ""
        self.start_time = None
        self.end_time = None
        self.test_active = False
        self.user_input = ""
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
        #self.type_text(banner, delay=0.002)
        self.type_text(banner,delay=0)

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
                    print(f"✅ You selected {self.selected_level.capitalize()} level.")
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

    def get_text(self):
        """Fetch text based on selected difficulty level and time"""
        # Calculate approximate word count needed (150 WPM = 2.5 words/second)
        target_word_count = int(self.selected_time * 2.5)
        
        texts = {
            'beginner': [
                "The sun rises in the east every morning. Birds sing sweet melodies in the trees. Children play in the park with their friends. Life is beautiful and simple.",
                "Today is a wonderful day to practice typing. Keep your fingers moving steadily across the keyboard. Focus on accuracy first, then speed will follow naturally.",
                "Reading books helps expand your knowledge. Walking in nature brings peace to the mind. Drinking water is essential for good health. Regular exercise keeps you fit.",
                "Music brings joy to everyone's life. Dancing makes people happy and energetic. Cooking is both an art and science. Learning new skills is always rewarding.",
                "Time passes quickly when you're having fun. Family gatherings create lasting memories. Friendship is a precious gift to treasure. Laughter is the best medicine."
            ],
            'intermediate': [
                "On Tuesday, Sarah visited the local market & bought: fresh vegetables, fruits, and bread! The total cost was $45.75, which seemed reasonable.",
                "Have you ever wondered why typing skills are so important? In today's digital age, fast & accurate typing can save hours of time!",
                "The weather forecast predicts 75% chance of rain & thunderstorms tomorrow; don't forget your umbrella! Temperature will range from 18°C to 25°C.",
                "Mr. Smith's presentation impressed everyone - his charts showed 45% growth in Q2! The team celebrated with pizza & refreshments later.",
                "The museum's new exhibit features artwork from the 1800s & early 1900s; tickets cost $22.50 for adults, $15.75 for students."
            ],
            'advanced': [
                "In Q1 2024, company XYZ reported 187.5% growth, processing @250,000 transactions/day! The CEO announced $2.5M investment in AI & ML tools.",
                "According to recent studies, ~75% of professionals type >65 WPM; however, only 15% achieve >100 WPM. Want to join the top 5%?",
                "Project #A-123 requires completion by 15/03/2024; estimated budget: $750K (+/- 10%). Contact support@company.com for queries.",
                "In 2023, global tech spending reached $4.5T (€4.1T); AI investments grew by 235%! Average ROI: 180% across 500+ companies.",
                "Database query optimized from O(n²) to O(log n), improving performance by 400%! Server load decreased from 85% to 23.5%."
            ],
            'expert': [
                "def optimize_performance(data: List[int]) -> float:\n    return sum(x * 1.5 for x in data if x > 0) # O(n) complexity",
                "async def process_data(queue: asyncio.Queue) -> Dict[str, Any]:\n    while not queue.empty():\n        item = await queue.get()",
                "class DatabaseManager:\n    def __init__(self, config: Dict):\n        self.pool = await create_pool(**config)\n        self.cache = LRUCache(1000)",
                "@decorator(param='value')\ndef handle_request(request: Request) -> Response:\n    try:\n        data = validate_input(request.data)\n    except ValidationError as e:",
                "from typing import Optional, Union\n\nclass Node[T]:\n    def __init__(self, value: T, next: Optional['Node[T]'] = None):\n        self.value = value"
            ]
        }

        selected_text = random.choice(texts[self.selected_level])
        
        # Adjust length by combining multiple texts if needed
        current_words = selected_text.split()
        while len(current_words) < target_word_count:
            additional_text = random.choice(texts[self.selected_level])
            current_words.extend(additional_text.split())
        
        # Trim to target length
        self.current_text = ' '.join(current_words[:target_word_count])

    def display_text_and_start(self):
        """Display the text to type"""
        self.clear_screen()
        self.display_banner()
        print("\nSelected Level:", self.selected_level.capitalize())
        print("Time Duration:", self.selected_time, "seconds")
        print("\n" + "="*70)
        print("\nType the following text:")
        print("\n" + "="*70 + "\n")
        print(self.current_text)
        print("\n" + "="*70)
        input("Press Enter when you're ready to start...")
        self.start_typing_test()

    def start_typing_test(self):
        self.clear_screen()
        time_remaining = self.selected_time
        print(f"Level: {self.selected_level.capitalize()} | Time: {self.selected_time} seconds")
        print("=" * 70)
        print(self.current_text)
        print("=" * 70)
        print("Start typing below. Press Ctrl+C to finish early.\n")

        self.start_time = time.time()
        self.test_active = True

        # Threading allows timer and input to run concurrently
        # Daemon ensures threads exit when main program exits
        timer_thread = threading.Thread(target=self.time_remaining)
        timer_thread.daemon = True
        timer_thread.start()

        input_thread = threading.Thread(target=self.time_countdown)
        input_thread.daemon = True
        input_thread.start()

        try:
            self.user_input = input()
        except KeyboardInterrupt:
            pass
        finally:
            self.test_active = False
            self.end_time = time.time()

    def time_countdown(self):
        """Countdown timer for the typing test"""
        start_timer = time.time()
        while self.test_active and (time.time() - start_timer) < self.selected_time:
            time.sleep(1)
        
        if self.test_active:
            self.test_active = False
            print("\n\n⏰ TIME'S UP!")
            # To interrupt input() in main thread
            try:
                if os.name == 'posix':
                    import sys
                    import termios
                    termios.tcflush(sys.stdin, termios.TCIFLUSH)
                else:
                    import msvcrt  # For Windows
                    if msvcrt.kbhit():
                        msvcrt.getch()
            except:
                pass

        self.calculate_results()

    def time_remaining(self):
        """Display remaining time every second"""
        import shutil
        rows, columns = shutil.get_terminal_size()
        while self.test_active:
            elapsed = int(time.time() - self.start_time)
            remaining = self.selected_time - elapsed
            if remaining < 0:
                remaining = 0
            # Move cursor to bottom line, clear the line, print timer, restore cursor
            sys.stdout.write(f"\0337\033[{rows};1H\033[K⏳ Time remaining: {remaining} seconds\0338")
            sys.stdout.flush()
            time.sleep(1)
        # Clear timer line after test ends
        sys.stdout.write(f"\0337\033[{rows};1H\033[K\0338")
        sys.stdout.flush()
        
    def calculate_results(self):
        """Calculate and return typing statistics"""
        actual_time = self.end_time - self.start_time

        # Calculate character-by-character comparison
        typed_chars = len(self.user_input)
        original_chars = len(self.current_text)
        
        # Calculate correct characters and errors
        correct_chars = 0
        min_length = min(typed_chars, original_chars)
        for i in range(min_length):
            if self.user_input[i] == self.current_text[i]:
                correct_chars += 1
        
        # Count actual words
        original_words = len(self.current_text.split())
        typed_words = len(self.user_input.split())
        
        # Calculate correct words
        original_word_list = self.current_text.split()
        typed_word_list = self.user_input.split()
        correct_words = 0
        for i in range(min(len(original_word_list), len(typed_word_list))):
            if typed_word_list[i] == original_word_list[i]:
                correct_words += 1
        
        # Calculate WPM using actual words typed
        wpm = (correct_words / actual_time) * 60 if actual_time > 0 else 0
        
        # Calculate accuracy percentage
        accuracy = (correct_chars / original_chars * 100) if original_chars > 0 else 0
        
        # Calculate total errors (character level)
        errors = typed_chars - correct_chars

        return {
            'wpm': round(wpm, 2),
            'accuracy': round(accuracy, 2),
            'typed_chars': typed_chars,
            'correct_chars': correct_chars,
            'errors': errors,
            'time_taken': round(actual_time, 2),
            'original_length': original_chars,
            'correct_words': correct_words,
            'total_words': original_words
        }

    def display_results(self, stats):
        pass

    def run(self):
        try:
            while True:
                self.clear_screen()
                self.display_banner()

                name = input("Enter your name: ")
                print(f"\nHello, {name}! Text your typing speed in terminal\n")

                if not self.get_difficulty_level():
                    continue
                if not self.get_time():
                    continue

                self.get_text()
                self.display_text_and_start()

                stats = self.calculate_results()
                self.display_results(stats)

                print("\nWould you like to try again? (y/n)", end=" ")
                if input().lower().strip() not in ['y', 'yes']:
                    break

        except KeyboardInterrupt:
            pass
        finally:
            print("\n\nThank you for using Terminal Typewriter. Goodbye!")


def main():
    app = Typewriter()
    app.run()

if __name__ == "__main__":
    main()