import json
import time
from pathlib import Path

DB_FILE = Path("data/context_history.json")


def save_context(symbol, score, status):
    DB_FILE.parent.mkdir(exist_ok=True)
    data = []

    if DB_FILE.exists():
        data = json.loads(DB_FILE.read_text())

    data.append({
        "symbol": symbol,
        "score": score,
        "status": status,
        "timestamp": int(time.time())
    })

    DB_FILE.write_text(json.dumps(data, indent=2))


def load_context(symbol, hours=72):
    if not DB_FILE.exists():
        return []

    now = int(time.time())
    cutoff = now - hours * 3600

    data = json.loads(DB_FILE.read_text())
    return [
        x for x in data
        if x["symbol"] == symbol and x["timestamp"] >= cutoff
    ]