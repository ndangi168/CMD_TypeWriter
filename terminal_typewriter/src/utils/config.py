import json
import os
from typing import Dict, Any, Optional


class ConfigManager:
    def __init__(self, config_dir: Optional[str] = None) -> None:
        if config_dir is None:
            # Use project config directory
            config_dir = os.path.join(os.getcwd(), "terminal_typewriter", "config")
        self.config_dir = config_dir
        os.makedirs(config_dir, exist_ok=True)
        
        self.settings_file = os.path.join(config_dir, "user_settings.json")
        self.themes_file = os.path.join(config_dir, "themes.json")
        self.default_settings_file = os.path.join(config_dir, "default_settings.json")
        
        self._settings: Dict[str, Any] = {}
        self._themes: Dict[str, Any] = {}
        self._load_all()

    def _load_all(self) -> None:
        self._load_default_settings()
        self._load_themes()
        self._load_user_settings()

    def _load_default_settings(self) -> None:
        defaults = {
            "default_difficulty": "beginner",
            "default_duration": 60,
            "default_theme": "default",
            "auto_save_sessions": True,
            "show_live_stats": True,
            "wpm_target": 60,
            "user_name": "Guest"
        }
        
        if os.path.exists(self.default_settings_file):
            try:
                with open(self.default_settings_file, 'r') as f:
                    loaded = json.load(f)
                    defaults.update(loaded)
            except (json.JSONDecodeError, IOError):
                pass
        
        # Save defaults if file doesn't exist
        if not os.path.exists(self.default_settings_file):
            with open(self.default_settings_file, 'w') as f:
                json.dump(defaults, f, indent=2)
        
        self._default_settings = defaults

    def _load_themes(self) -> None:
        default_themes = {
            "default": {
                "name": "Default",
                "colors": {
                    "header": "white",
                    "text": "white",
                    "correct": "green",
                    "incorrect": "red",
                    "caret": "yellow"
                }
            },
            "dark": {
                "name": "Dark",
                "colors": {
                    "header": "cyan",
                    "text": "white",
                    "correct": "green",
                    "incorrect": "red",
                    "caret": "yellow"
                }
            },
            "bright": {
                "name": "Bright",
                "colors": {
                    "header": "blue",
                    "text": "black",
                    "correct": "green",
                    "incorrect": "red",
                    "caret": "magenta"
                }
            }
        }
        
        if os.path.exists(self.themes_file):
            try:
                with open(self.themes_file, 'r') as f:
                    loaded = json.load(f)
                    default_themes.update(loaded)
            except (json.JSONDecodeError, IOError):
                pass
        
        # Save themes if file doesn't exist
        if not os.path.exists(self.themes_file):
            with open(self.themes_file, 'w') as f:
                json.dump(default_themes, f, indent=2)
        
        self._themes = default_themes

    def _load_user_settings(self) -> None:
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    self._settings = json.load(f)
            except (json.JSONDecodeError, IOError):
                self._settings = {}
        else:
            self._settings = {}

    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value, falling back to defaults."""
        return self._settings.get(key, self._default_settings.get(key, default))

    def set(self, key: str, value: Any) -> None:
        """Set a setting value."""
        self._settings[key] = value

    def save_settings(self) -> None:
        """Save current settings to file."""
        with open(self.settings_file, 'w') as f:
            json.dump(self._settings, f, indent=2)

    def get_theme(self, theme_name: Optional[str] = None) -> Dict[str, Any]:
        """Get theme configuration."""
        if theme_name is None:
            theme_name = self.get("default_theme", "default")
        return self._themes.get(theme_name, self._themes["default"])

    def list_themes(self) -> Dict[str, str]:
        """List available themes."""
        return {name: theme["name"] for name, theme in self._themes.items()}

    def reset_to_defaults(self) -> None:
        """Reset all settings to defaults."""
        self._settings = {}
        self.save_settings()