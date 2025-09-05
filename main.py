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
        print(f"Level: {self.selected_level.capitalize()} | Time: {self.selected_time} seconds | Time remaining: {time_remaining} seconds")
        print("=" * 70)
        print(self.current_text)
        print("=" * 70)
        print("Start typing below. Press Ctrl+C to finish early.\n")

        self.start_time = time.time()
        self.test_active = True

        # Thread Deamon to handle countdown
        input_thread = threading.Thread(target=self.time_countdown)
        input_thread.daemon = True
        input_thread.start()

        try:
            self.user_input = input("")
        except KeyboardInterrupt:
            print("\nTest interrupted by user.")
            pass
        finally:
            self.test_active = False
            self.end_time = time.time()

    def time_countdown(self):
        pass

    def run(self):
        self.clear_screen()
        self.display_banner()
        name = input("Enter your name: ")
        print(f"\nHello, {name}! Text your typing speed in terminal\n")
        self.get_difficulty_level()
        self.get_time()
        self.get_text()
        self.display_text_and_start()


def main():
    app = Typewriter()
    app.run()

if __name__ == "__main__":
    main()