from state import ProcurementState


def run(state: ProcurementState) -> dict:
    parsed = state["parsed_request"]
    routing = state["routing_result"]
    submitter = state.get("submitter")

    final_status = routing.get("final_status", "unknown")
    notifications = state["notification_result"].get("approver_notifications", [])

    if submitter:
        message = (
            f"Your request for {parsed.get('quantity')}x {parsed.get('product')} "
            f"has been {'APPROVED' if final_status == 'approved' else 'REJECTED'}."
        )
        notifications.append({"to": submitter["email"], "name": submitter["name"], "message": message})
        print(f"[Notify Submitter] → {submitter['email']}: {message}")

    return {"notification_result": {"approver_notifications": notifications[:-1], "submitter_notification": notifications[-1] if submitter else None}}
