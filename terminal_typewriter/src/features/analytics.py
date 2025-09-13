from typing import List, Dict, Any, Tuple
from statistics import mean, median


class Analytics:
    def __init__(self, sessions: List[Dict[str, Any]]) -> None:
        self.sessions = sessions

    def get_summary_stats(self) -> Dict[str, Any]:
        """Get overall summary statistics."""
        if not self.sessions:
            return {
                'total_sessions': 0,
                'total_time': 0,
                'best_wpm': 0,
                'avg_wpm': 0,
                'best_accuracy': 0,
                'avg_accuracy': 0,
                'total_errors': 0
            }
        
        wpm_values = [s.get('wpm', 0) for s in self.sessions]
        accuracy_values = [s.get('accuracy', 0) for s in self.sessions]
        durations = [s.get('duration', 0) for s in self.sessions]
        
        return {
            'total_sessions': len(self.sessions),
            'total_time': sum(durations),
            'best_wpm': max(wpm_values) if wpm_values else 0,
            'avg_wpm': round(mean(wpm_values), 2) if wpm_values else 0,
            'median_wpm': round(median(wpm_values), 2) if wpm_values else 0,
            'best_accuracy': max(accuracy_values) if accuracy_values else 0,
            'avg_accuracy': round(mean(accuracy_values), 2) if accuracy_values else 0,
            'median_accuracy': round(median(accuracy_values), 2) if accuracy_values else 0,
            'total_errors': sum(s.get('errors', 0) for s in self.sessions)
        }

    def get_progress_trends(self, sessions_limit: int = 10) -> Dict[str, Any]:
        """Get recent progress trends."""
        recent_sessions = self.sessions[:sessions_limit]  # Most recent sessions
        if len(recent_sessions) < 2:
            return {'trend': 'insufficient_data', 'message': 'Need at least 2 sessions to show trends'}
        
        recent_wpm = [s.get('wpm', 0) for s in recent_sessions]
        recent_accuracy = [s.get('accuracy', 0) for s in recent_sessions]
        
        # Calculate trends (simple linear trend)
        wpm_trend = "improving" if recent_wpm[0] > recent_wpm[-1] else "declining" if recent_wpm[0] < recent_wpm[-1] else "stable"
        accuracy_trend = "improving" if recent_accuracy[0] > recent_accuracy[-1] else "declining" if recent_accuracy[0] < recent_accuracy[-1] else "stable"
        
        wpm_change = recent_wpm[0] - recent_wpm[-1]
        accuracy_change = recent_accuracy[0] - recent_accuracy[-1]
        
        return {
            'wpm_trend': wpm_trend,
            'accuracy_trend': accuracy_trend,
            'wpm_change': round(wpm_change, 2),
            'accuracy_change': round(accuracy_change, 2),
            'sessions_analyzed': len(recent_sessions)
        }

    def get_difficulty_stats(self) -> Dict[str, Dict[str, float]]:
        """Get statistics by difficulty level."""
        difficulty_stats = {}
        
        for session in self.sessions:
            mode = session.get('mode', 'unknown')
            if mode not in difficulty_stats:
                difficulty_stats[mode] = {'wpm': [], 'accuracy': [], 'count': 0}
            
            difficulty_stats[mode]['wpm'].append(session.get('wpm', 0))
            difficulty_stats[mode]['accuracy'].append(session.get('accuracy', 0))
            difficulty_stats[mode]['count'] += 1
        
        # Calculate averages for each difficulty
        for mode, stats in difficulty_stats.items():
            if stats['wpm']:
                stats['avg_wpm'] = round(mean(stats['wpm']), 2)
                stats['avg_accuracy'] = round(mean(stats['accuracy']), 2)
                stats['best_wpm'] = max(stats['wpm'])
                stats['best_accuracy'] = max(stats['accuracy'])
            else:
                stats['avg_wpm'] = 0
                stats['avg_accuracy'] = 0
                stats['best_wpm'] = 0
                stats['best_accuracy'] = 0
            
            # Remove raw data, keep only summaries
            del stats['wpm']
            del stats['accuracy']
        
        return difficulty_stats

    def format_summary_report(self) -> str:
        """Format a human-readable summary report."""
        summary = self.get_summary_stats()
        trends = self.get_progress_trends()
        difficulty_stats = self.get_difficulty_stats()
        
        report = []
        report.append("📊 TYPING ANALYTICS REPORT")
        report.append("=" * 50)
        report.append("")
        
        # Overall stats
        report.append("🎯 Overall Performance:")
        report.append(f"  Total Sessions: {summary['total_sessions']}")
        report.append(f"  Total Time: {summary['total_time']:.1f} seconds")
        report.append(f"  Best WPM: {summary['best_wpm']}")
        report.append(f"  Average WPM: {summary['avg_wpm']}")
        report.append(f"  Best Accuracy: {summary['best_accuracy']:.1f}%")
        report.append(f"  Average Accuracy: {summary['avg_accuracy']:.1f}%")
        report.append(f"  Total Errors: {summary['total_errors']}")
        report.append("")
        
        # Trends
        if trends.get('trend') != 'insufficient_data':
            report.append("📈 Recent Trends:")
            report.append(f"  WPM Trend: {trends['wpm_trend']} ({trends['wpm_change']:+.1f})")
            report.append(f"  Accuracy Trend: {trends['accuracy_trend']} ({trends['accuracy_change']:+.1f}%)")
            report.append(f"  Sessions Analyzed: {trends['sessions_analyzed']}")
        else:
            report.append("📈 Recent Trends: Insufficient data (need 2+ sessions)")
        report.append("")
        
        # Difficulty breakdown
        if difficulty_stats:
            report.append("🎮 Performance by Difficulty:")
            for mode, stats in difficulty_stats.items():
                report.append(f"  {mode.capitalize()}:")
                report.append(f"    Sessions: {stats['count']}")
                report.append(f"    Avg WPM: {stats['avg_wpm']}")
                report.append(f"    Best WPM: {stats['best_wpm']}")
                report.append(f"    Avg Accuracy: {stats['avg_accuracy']:.1f}%")
        
        return "\n".join(report)