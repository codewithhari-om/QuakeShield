
from datetime import datetime, timezone
import json


def build_event_message(result, station_id="QS-001"):
    """Convert a processing result into a JSON-ready message."""

    candidates = result.get("ranked_candidates", [])

    events = []

    for candidate in candidates:
        events.append({
            "start_time_seconds": candidate["start_time_seconds"],
            "end_time_seconds": candidate["end_time_seconds"],
            "score": candidate["score"],
            "priority": candidate["priority"],
            "quality_flags": candidate["quality"]["quality_flags"],
            "features": candidate["features"],
            "onset_features": candidate.get("onset_features"),
        })

    return {
        "station_id": station_id,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "sampling_rate_hz": result["sampling_rate"],
        "candidate_count": len(events),
        "candidates": events,
        "message_type": "candidate_analysis",
        "warning": (
            "Experimental candidate detections only; "
            "not a confirmed earthquake alert."
        ),
    }


def save_event_message(message, output_path):
    """Save the message as formatted JSON."""

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(message, file, indent=2, allow_nan=False)
