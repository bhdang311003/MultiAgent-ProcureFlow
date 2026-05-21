from state import ProcurementState
from mock_data import DEPARTMENT_BUDGETS

def run(state: ProcurementState) -> dict:
    parsed = state["parsed_request"]
    department = parsed.get("department")
    amount = parsed.get("budget_vnd") or 0

    if department not in DEPARTMENT_BUDGETS:
        return {"budget_result": {
            "approved": False,
            "reason": f"Department '{department}' not found.",
            "remaining_budget": None,
            "requested": amount,
        }}

    dept = DEPARTMENT_BUDGETS[department]
    remaining = dept["total"] - dept["spent"]
    approved = amount <= remaining

    return {"budget_result": {
        "approved": approved,
        "reason": "Budget sufficient." if approved else f"Exceeds remaining budget ({remaining:,} VND).",
        "remaining_budget": remaining,
        "requested": amount,
    }}
