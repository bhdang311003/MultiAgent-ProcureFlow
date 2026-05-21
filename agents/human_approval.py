from langgraph.types import interrupt
from state import ProcurementState


def run(state: ProcurementState) -> dict:
    routing = state["routing_result"]
    parsed = state["parsed_request"]

    # Graph dừng tại đây, chờ từng approver quyết định
    decisions = []
    for approver in routing.get("approvers", []):
        decision = interrupt({
            "approver": approver["name"],
            "email": approver["email"],
            "request": f"{parsed.get('quantity')}x {parsed.get('product')} — {parsed.get('budget_vnd'):,} VND",
            "action": "approve or reject",
        })
        decisions.append({
            "approver": approver["name"],
            "decision": decision,
        })
        if decision == "reject":
            break

    approved = all(d["decision"] == "approve" for d in decisions)
    return {"routing_result": {
        **routing,
        "decisions": decisions,
        "final_status": "approved" if approved else "rejected",
    }}
