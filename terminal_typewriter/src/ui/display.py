import os
import sys


class DisplayManager:
    def clear(self) -> None:
        os.system('clear' if os.name == 'posix' else 'cls')

    def banner(self) -> None:
        banner = r"""
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                          🎯 TERMINAL TYPEWRITER 🎯                           ║
    ║                        Calculate Your Typing Speed                           ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)

    def show_text(self, level: str, duration: int, text: str) -> None:
        print("\nSelected Level:", level.capitalize())
        print("Time Duration:", duration, "seconds")
        print("\n" + "=" * 70)
        print("\nType the following text:")
        print("\n" + "=" * 70 + "\n")
        print(text)
        print("\n" + "=" * 70)

    def show_results(self, result) -> None:
        print("\n🎉 TYPING TEST COMPLETED! 🎉")
        print("=" * 50)
        print("\n📊 Statistics:")
        print(f"⚡ Words Per Minute: {result.wpm}")
        print(f"🎯 Accuracy: {result.accuracy}%")
        print(f"⏱️  Time: {result.duration_seconds} seconds")
        print(f"❌ Errors: {result.errors}")
        print(f"📝 Total chars: {result.text_length}")
        print("\n" + "=" * 50)