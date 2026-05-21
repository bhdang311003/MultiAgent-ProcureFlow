import json
import os
from datetime import datetime

MEMORY_FILE = "procurement_history.json"
ACTIVE_FILE = "active_requests.json"


def load_active_requests() -> list:
    if not os.path.exists(ACTIVE_FILE):
        return []
    with open(ACTIVE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def add_active_request(thread_id: str, product: str) -> None:
    active = load_active_requests()
    active.append({"thread_id": thread_id, "product": product})
    with open(ACTIVE_FILE, "w", encoding="utf-8") as f:
        json.dump(active, f, ensure_ascii=False, indent=2)


def remove_active_request(thread_id: str) -> None:
    active = [r for r in load_active_requests() if r["thread_id"] != thread_id]
    with open(ACTIVE_FILE, "w", encoding="utf-8") as f:
        json.dump(active, f, ensure_ascii=False, indent=2)


def load_history() -> list:
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_request(parsed_request: dict, final_status: str) -> None:
    history = load_history()
    history.append({
        "timestamp": datetime.now().isoformat(),
        "product": parsed_request.get("product"),
        "quantity": parsed_request.get("quantity"),
        "department": parsed_request.get("department"),
        "budget_vnd": parsed_request.get("budget_vnd"),
        "final_status": final_status,
    })
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def get_recent_history(department: str = None, limit: int = 10) -> list:
    history = load_history()
    if department:
        history = [h for h in history if h.get("department") == department]
    return history[-limit:]
