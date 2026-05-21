from state import ProcurementState


def run(state: ProcurementState) -> dict:
    parsed = state["parsed_request"]
    routing = state["routing_result"]
    risk = state["risk_result"]

    notifications = []
    for approver in routing.get("approvers", []):
        message = (
            f"Approval required: {parsed.get('quantity')}x {parsed.get('product')} "
            f"for {parsed.get('department')} — "
            f"Budget: {parsed.get('budget_vnd'):,} VND — "
            f"Risk: {risk.get('risk_score', 'unknown').upper()}"
        )
        notifications.append({"to": approver["email"], "name": approver["name"], "message": message})
        print(f"[Notify Approver] → {approver['email']}: {message}")

    return {"notification_result": {"approver_notifications": notifications}}
