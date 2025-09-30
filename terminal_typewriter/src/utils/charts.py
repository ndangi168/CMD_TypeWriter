from typing import List, Dict, Any, Tuple
from statistics import mean


class ASCIIChart:
    """Generate ASCII charts for data visualization."""
    
    def __init__(self, width: int = 60, height: int = 15):
        self.width = width
        self.height = height

    def generate_line_chart(self, data: List[float], title: str = "", x_labels: List[str] = None) -> str:
        """Generate a line chart from data points."""
        if not data:
            return f"{title}\n(No data available)\n"
        
        # Normalize data to fit chart height
        min_val = min(data)
        max_val = max(data)
        if max_val == min_val:
            # All values are the same
            normalized_data = [self.height // 2] * len(data)
        else:
            normalized_data = [
                int((val - min_val) / (max_val - min_val) * (self.height - 2)) + 1
                for val in data
            ]
        
        # Create chart grid
        chart_lines = []
        
        # Add title
        if title:
            chart_lines.append(f" {title}")
            chart_lines.append(" " + "─" * len(title))
        
        # Generate chart from top to bottom
        for y in range(self.height, 0, -1):
            line = ""
            for i, val in enumerate(normalized_data):
                if i >= self.width:
                    break
                
                if val >= y:
                    line += "█"
                elif val == y - 1:
                    line += "▄"
                else:
                    line += " "
            
            # Add y-axis label (every 3rd line)
            if y % 3 == 0 or y == self.height or y == 1:
                label = f"{min_val + (max_val - min_val) * (y - 1) / (self.height - 1):.1f}"
                chart_lines.append(f"{label:>6} │{line}")
            else:
                chart_lines.append(f"      │{line}")
        
        # Add x-axis
        chart_lines.append("      └" + "─" * min(len(data), self.width))
        
        # Add x-axis labels if provided
        if x_labels:
            label_line = "       "
            for i in range(0, min(len(x_labels), self.width), max(1, self.width // 8)):
                if i < len(x_labels):
                    label_line += f"{x_labels[i]:<8}"
            chart_lines.append(label_line)
        
        return "\n".join(chart_lines)

    def generate_bar_chart(self, data: Dict[str, float], title: str = "") -> str:
        """Generate a bar chart from key-value data."""
        if not data:
            return f"{title}\n(No data available)\n"
        
        # Find max value for scaling
        max_val = max(data.values()) if data.values() else 1
        
        chart_lines = []
        
        # Add title
        if title:
            chart_lines.append(f" {title}")
            chart_lines.append(" " + "─" * len(title))
        
        # Generate bars
        for key, value in data.items():
            # Calculate bar length
            bar_length = int((value / max_val) * (self.width - 15)) if max_val > 0 else 0
            bar = "█" * bar_length
            
            # Format the line
            chart_lines.append(f"{key:>12} │{bar} {value:.1f}")
        
        return "\n".join(chart_lines)

    def generate_progress_chart(self, current: float, target: float, title: str = "") -> str:
        """Generate a progress bar chart."""
        if target <= 0:
            percentage = 0
        else:
            percentage = min(100, (current / target) * 100)
        
        # Calculate filled and empty segments
        filled_segments = int(percentage / 100 * (self.width - 20))
        empty_segments = (self.width - 20) - filled_segments
        
        progress_bar = "█" * filled_segments + "░" * empty_segments
        
        chart_lines = []
        if title:
            chart_lines.append(f" {title}")
            chart_lines.append(" " + "─" * len(title))
        
        chart_lines.append(f" Progress: [{progress_bar}] {percentage:.1f}%")
        chart_lines.append(f" Current: {current:.1f} / Target: {target:.1f}")
        
        return "\n".join(chart_lines)

    def generate_wpm_trend_chart(self, sessions: List[Dict[str, Any]], title: str = "WPM Trend") -> str:
        """Generate a WPM trend chart from session data."""
        if not sessions:
            return f"{title}\n(No sessions available)\n"
        
        # Extract WPM data (most recent first, so reverse for chronological order)
        wpm_data = [s.get('wpm', 0) for s in reversed(sessions[-20:])]  # Last 20 sessions
        
        # Generate labels (session numbers)
        x_labels = [f"S{i+1}" for i in range(len(wpm_data))]
        
        return self.generate_line_chart(wpm_data, title, x_labels)

    def generate_accuracy_trend_chart(self, sessions: List[Dict[str, Any]], title: str = "Accuracy Trend") -> str:
        """Generate an accuracy trend chart from session data."""
        if not sessions:
            return f"{title}\n(No sessions available)\n"
        
        # Extract accuracy data
        accuracy_data = [s.get('accuracy', 0) for s in reversed(sessions[-20:])]  # Last 20 sessions
        
        # Generate labels
        x_labels = [f"S{i+1}" for i in range(len(accuracy_data))]
        
        return self.generate_line_chart(accuracy_data, title, x_labels)

    def generate_difficulty_performance_chart(self, sessions: List[Dict[str, Any]], title: str = "Performance by Difficulty") -> str:
        """Generate a bar chart showing performance by difficulty level."""
        if not sessions:
            return f"{title}\n(No sessions available)\n"
        
        # Group sessions by difficulty
        difficulty_stats = {}
        for session in sessions:
            mode = session.get('mode', 'unknown')
            if mode not in difficulty_stats:
                difficulty_stats[mode] = []
            difficulty_stats[mode].append(session.get('wpm', 0))
        
        # Calculate average WPM for each difficulty
        difficulty_avg = {}
        for mode, wpm_list in difficulty_stats.items():
            if wpm_list:
                difficulty_avg[mode] = mean(wpm_list)
        
        return self.generate_bar_chart(difficulty_avg, title)
