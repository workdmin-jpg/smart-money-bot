from dashboard.storage import load_context


def build_context_timeline(symbol):
    history = load_context(symbol)

    if not history:
        return None

    timeline = []
    for h in history:
        timeline.append({
            "time": h["timestamp"],
            "score": h["score"],
            "status": h["status"]
        })

    return timeline