# Terminal Typewriter 🎯

A comprehensive terminal-based typing speed test and practice application built with Python. Track your typing progress, unlock achievements, and improve your typing skills with real-time feedback and detailed analytics.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Features

### 🎮 Core Functionality
- **Real-time Typing Tests** - Live WPM and accuracy tracking
- **Multiple Difficulty Levels** - Beginner, Intermediate, Advanced, and Expert
- **Flexible Duration** - 30 seconds to custom time limits
- **Session Replay** - Watch your typing sessions with keystroke timing
- **Curses UI** - Smooth, responsive terminal interface

### 📊 Analytics & Progress
- **Detailed Statistics** - WPM, accuracy, error tracking, and trends
- **Progress Reports** - Performance by difficulty level and over time
- **Session History** - Complete log of all typing sessions
- **Achievement System** - 14 badges for milestones and goals

### 🏆 Achievements
- **Speed Milestones** - 30, 50, 75, 100 WPM achievements
- **Accuracy Goals** - 95% and 99% precision badges
- **Practice Rewards** - 10, 50, 100 session milestones
- **Time Investment** - 1 hour and 5 hour practice achievements
- **Versatility** - Complete all difficulty levels
- **Consistency** - 5-day practice streak

## Usage

1. **Launch:** `python main.py`
2. **Enter your name** (saved for future sessions)
3. **Choose from menu:**
   - Start Typing Test (standard or curses mode)
   - View Session History
   - Replay Last Session
   - Analytics & Progress
   - Achievements
   - Settings

### Test Options
- **Difficulty:** Beginner → Intermediate → Advanced → Expert (code)
- **Duration:** 30s, 1min, 2min, or custom
- **Modes:** Standard terminal or enhanced curses UI

## Installation

### Prerequisites
- Python 3.7+
- Terminal with curses support (Linux/macOS) or Windows Terminal

### Setup
```bash
# Clone/download the project
cd terminal_typewriter

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Windows Users
If curses doesn't work on Windows:
```bash
pip install windows-curses
```

## Project Structure

```
terminal_typewriter/
├── main.py                    # Application entry point
├── requirements.txt           # Dependencies
├── README.md                 # This file
│
├── src/
│   ├── core/                 # Core typing logic
│   ├── ui/                   # User interface
│   ├── data/                 # Data persistence
│   ├── features/             # Extended functionality
│   └── utils/                # Utilities
│
├── config/                   # Configuration files
├── data/                     # Database and text storage
└── tests/                    # Test suite
```

## Configuration

### Settings Menu
- Default difficulty and duration
- Theme selection (Default, Dark, Bright)
- User name and preferences
- Auto-save sessions

### Themes
Customize colors for:
- Headers and text
- Correct/incorrect characters
- Cursor/caret

## Development

### Running Tests
```bash
python -m pytest tests/ -v
```

### Adding Features
- **New achievements:** Edit `config/achievements.json`
- **Text content:** Add to `data/texts/` and update `TextManager`
- **Themes:** Modify `config/themes.json`

## Troubleshooting

**Curses issues:** Use standard mode instead of curses mode
**Database errors:** Check `data/database/` permissions
**Import errors:** Ensure you're in the project directory
**Performance:** Use standard mode on older terminals

## License

Open source - see LICENSE file for details.

---

**Happy Typing!** 🚀 Start practicing and unlock your first achievement!
