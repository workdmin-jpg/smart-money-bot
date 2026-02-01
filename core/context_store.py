# core/context_store.py

import json
import time
import os

STORE_FILE = "context_store.json"
MAX_AGE_SECONDS = 3 * 24 * 60 * 60  # 72 ساعة

def _load_store():
    if not os.path.exists(STORE_FILE):
        return {}

    with open(STORE_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return {}

def _save_store(data):
    with open(STORE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def _cleanup_old_entries(store):
    now = time.time()
    to_delete = []

    for symbol, info in store.items():
        if now - info.get("timestamp", 0) > MAX_AGE_SECONDS:
            to_delete.append(symbol)

    for s in to_delete:
        del store[s]

    return store

def should_send_signal(symbol, new_score):
    """
    ❗ لا يرسل إشارة جديدة إلا إذا:
    - لا يوجد سجل سابق
    - أو تحسّن Context Score
    """
    store = _load_store()
    store = _cleanup_old_entries(store)

    old = store.get(symbol)

    if not old:
        return True

    old_score = old.get("score", 0)
    return new_score > old_score

def update_context_score(symbol, score):
    store = _load_store()
    store = _cleanup_old_entries(store)

    store[symbol] = {
        "score": score,
        "timestamp": time.time()
    }

    _save_store(store)