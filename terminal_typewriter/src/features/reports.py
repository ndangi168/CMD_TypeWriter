from typing import List, Dict, Any


def format_history_table(rows: List[Dict[str, Any]]) -> str:
    if not rows:
        return "No sessions found."
    headers = ["#", "ID", "Timestamp", "Mode", "Dur(s)", "WPM", "Acc(%)", "Err"]
    lines = [" | ".join(headers), "-" * 80]
    for idx, r in enumerate(rows, 1):
        lines.append(
            " | ".join(
                [
                    str(idx),
                    r.get("id", "")[:8],
                    str(r.get("timestamp", ""))[:19],
                    str(r.get("mode", "")),
                    str(int(r.get("duration", 0))),
                    str(r.get("wpm", 0)),
                    str(r.get("accuracy", 0)),
                    str(r.get("errors", 0)),
                ]
            )
        )
    return "\n".join(lines)