import json
import os
from typing import List, Dict, Any, Set
from datetime import datetime

from ..data.storage import StorageManager
from ..utils.helpers import now_utc_iso


class AchievementSystem:
    def __init__(self, storage: StorageManager, config_dir: str = None) -> None:
        self.storage = storage
        if config_dir is None:
            config_dir = os.path.join(os.getcwd(), "terminal_typewriter", "config")
        self.config_dir = config_dir
        self.achievements_file = os.path.join(config_dir, "achievements.json")
        
        self.achievements = self._load_achievements()
        self.unlocked_achievements = self._load_unlocked_achievements()

    def _load_achievements(self) -> Dict[str, Dict[str, Any]]:
        """Load achievement definitions from config file."""
        default_achievements = {
            "first_session": {
                "name": "First Steps",
                "description": "Complete your first typing session",
                "icon": "🎯",
                "condition": "sessions >= 1"
            },
            "speed_30": {
                "name": "Getting Faster",
                "description": "Achieve 30 WPM in a session",
                "icon": "⚡",
                "condition": "max_wpm >= 30"
            },
            "speed_50": {
                "name": "Speed Demon",
                "description": "Achieve 50 WPM in a session",
                "icon": "🚀",
                "condition": "max_wpm >= 50"
            },
            "speed_75": {
                "name": "Lightning Fast",
                "description": "Achieve 75 WPM in a session",
                "icon": "⚡⚡",
                "condition": "max_wpm >= 75"
            },
            "speed_100": {
                "name": "Typing Master",
                "description": "Achieve 100 WPM in a session",
                "icon": "🏆",
                "condition": "max_wpm >= 100"
            },
            "accuracy_95": {
                "name": "Precision",
                "description": "Achieve 95% accuracy in a session",
                "icon": "🎯",
                "condition": "max_accuracy >= 95"
            },
            "accuracy_99": {
                "name": "Perfect Aim",
                "description": "Achieve 99% accuracy in a session",
                "icon": "💯",
                "condition": "max_accuracy >= 99"
            },
            "sessions_10": {
                "name": "Dedicated",
                "description": "Complete 10 typing sessions",
                "icon": "📚",
                "condition": "sessions >= 10"
            },
            "sessions_50": {
                "name": "Committed",
                "description": "Complete 50 typing sessions",
                "icon": "🔥",
                "condition": "sessions >= 50"
            },
            "sessions_100": {
                "name": "Expert",
                "description": "Complete 100 typing sessions",
                "icon": "👑",
                "condition": "sessions >= 100"
            },
            "time_1hour": {
                "name": "Marathon",
                "description": "Spend 1 hour total typing",
                "icon": "⏰",
                "condition": "total_time >= 3600"
            },
            "time_5hours": {
                "name": "Endurance",
                "description": "Spend 5 hours total typing",
                "icon": "🏃",
                "condition": "total_time >= 18000"
            },
            "all_difficulties": {
                "name": "Versatile",
                "description": "Complete sessions in all difficulty levels",
                "icon": "🌟",
                "condition": "all_difficulties_completed"
            },
            "streak_5": {
                "name": "Consistent",
                "description": "Complete 5 sessions in a row (daily)",
                "icon": "📅",
                "condition": "streak >= 5"
            }
        }
        
        if os.path.exists(self.achievements_file):
            try:
                with open(self.achievements_file, 'r') as f:
                    loaded = json.load(f)
                    default_achievements.update(loaded)
            except (json.JSONDecodeError, IOError):
                pass
        
        # Save achievements if file doesn't exist
        if not os.path.exists(self.achievements_file):
            with open(self.achievements_file, 'w') as f:
                json.dump(default_achievements, f, indent=2)
        
        return default_achievements

    def _load_unlocked_achievements(self) -> Set[str]:
        """Load unlocked achievements from database."""
        # For now, we'll calculate unlocked achievements dynamically
        # In a full implementation, you'd store these in the database
        return set()

    def check_achievements(self, sessions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Check which achievements should be unlocked based on current stats."""
        if not sessions:
            return []
        
        # Calculate stats
        stats = self._calculate_stats(sessions)
        new_achievements = []
        
        for achievement_id, achievement in self.achievements.items():
            if achievement_id in self.unlocked_achievements:
                continue
                
            if self._evaluate_condition(achievement["condition"], stats, sessions):
                new_achievements.append({
                    "id": achievement_id,
                    "name": achievement["name"],
                    "description": achievement["description"],
                    "icon": achievement["icon"],
                    "unlocked_at": now_utc_iso()
                })
                self.unlocked_achievements.add(achievement_id)
        
        return new_achievements

    def _calculate_stats(self, sessions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate statistics from sessions."""
        if not sessions:
            return {
                "sessions": 0,
                "max_wpm": 0,
                "max_accuracy": 0,
                "total_time": 0,
                "difficulties_completed": set(),
                "streak": 0
            }
        
        wpm_values = [s.get('wpm', 0) for s in sessions]
        accuracy_values = [s.get('accuracy', 0) for s in sessions]
        durations = [s.get('duration', 0) for s in sessions]
        difficulties = set(s.get('mode', '') for s in sessions)
        
        # Calculate streak (consecutive days with sessions)
        streak = self._calculate_streak(sessions)
        
        return {
            "sessions": len(sessions),
            "max_wpm": max(wpm_values) if wpm_values else 0,
            "max_accuracy": max(accuracy_values) if accuracy_values else 0,
            "total_time": sum(durations),
            "difficulties_completed": difficulties,
            "streak": streak
        }

    def _calculate_streak(self, sessions: List[Dict[str, Any]]) -> int:
        """Calculate current streak of consecutive days with sessions."""
        if not sessions:
            return 0
        
        # Sort sessions by timestamp (most recent first)
        sorted_sessions = sorted(sessions, key=lambda x: x.get('timestamp', ''), reverse=True)
        
        # Group by date
        dates = set()
        for session in sorted_sessions:
            timestamp = session.get('timestamp', '')
            if timestamp:
                date = timestamp.split('T')[0]  # Extract date part
                dates.add(date)
        
        # Calculate consecutive days
        sorted_dates = sorted(dates, reverse=True)
        streak = 0
        current_date = datetime.now().date()
        
        for date_str in sorted_dates:
            session_date = datetime.fromisoformat(date_str).date()
            if session_date == current_date or (current_date - session_date).days == 1:
                streak += 1
                current_date = session_date
            else:
                break
        
        return streak

    def _evaluate_condition(self, condition: str, stats: Dict[str, Any], sessions: List[Dict[str, Any]]) -> bool:
        """Evaluate achievement condition."""
        if condition == "all_difficulties_completed":
            required_difficulties = {"beginner", "intermediate", "advanced", "expert"}
            return required_difficulties.issubset(stats["difficulties_completed"])
        
        # Simple condition evaluation (can be expanded)
        try:
            # Replace variables with actual values
            eval_condition = condition
            eval_condition = eval_condition.replace("sessions", str(stats["sessions"]))
            eval_condition = eval_condition.replace("max_wpm", str(stats["max_wpm"]))
            eval_condition = eval_condition.replace("max_accuracy", str(stats["max_accuracy"]))
            eval_condition = eval_condition.replace("total_time", str(stats["total_time"]))
            eval_condition = eval_condition.replace("streak", str(stats["streak"]))
            
            return eval(eval_condition)
        except:
            return False

    def get_unlocked_achievements(self) -> List[Dict[str, Any]]:
        """Get list of unlocked achievements."""
        unlocked = []
        for achievement_id in self.unlocked_achievements:
            if achievement_id in self.achievements:
                unlocked.append({
                    "id": achievement_id,
                    **self.achievements[achievement_id]
                })
        return unlocked

    def format_achievements_report(self) -> str:
        """Format achievements for display."""
        unlocked = self.get_unlocked_achievements()
        
        report = []
        report.append("🏆 ACHIEVEMENTS")
        report.append("=" * 50)
        
        if unlocked:
            report.append(f"\n✅ Unlocked ({len(unlocked)}):")
            for achievement in unlocked:
                report.append(f"  {achievement['icon']} {achievement['name']}")
                report.append(f"    {achievement['description']}")
        else:
            report.append("\n💪 No achievements unlocked yet!")
            report.append("Keep practicing to unlock your first achievement!")
        
        # Show progress on key achievements
        report.append(f"\n📊 Progress:")
        report.append(f"  Sessions completed: {len(self.unlocked_achievements)}")
        
        return "\n".join(report)