import os
import sys
from ..core.engine import TypingEngine


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

    def render_live(self, engine: TypingEngine, remaining_seconds: int) -> None:
        stats = engine.get_current_stats()
        print("\n" + "-" * 70)
        print(f"⏳ Time remaining: {remaining_seconds:>3} s  |  WPM: {stats.wpm:>5}  |  Acc: {stats.accuracy:>5}%  |  Chars: {stats.characters_typed}")
        print("-" * 70)
        buf = engine.get_buffer()
        caret = "|"
        # Show only last 120 characters of buffer for brevity
        snippet = buf[-120:]
        print(f"Your input: {snippet}{caret}")