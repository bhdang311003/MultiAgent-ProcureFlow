import json
from state import ProcurementState
from llm_client import call_llm
from memory import get_recent_history

RISK_PROMPT = """You are a procurement risk analyst. Analyze the purchase request and return ONLY a valid JSON object:
{
  "risk_score": "low" | "medium" | "high",
  "flags": ["list of issues found, empty if none"],
  "reasoning": "brief explanation"
}

Check for:
- Abnormal unit price (budget / quantity)
- Abnormal quantity for the department size
- Product mismatched with department (e.g. HR buying GPU servers)
- Unrealistic deadline
- Duplicate or suspicious requests based on procurement history"""


def run(state: ProcurementState) -> dict:
    parsed = state["parsed_request"]
    department = parsed.get("department")

    history = get_recent_history(department=department, limit=5)
    history_text = json.dumps(history, ensure_ascii=False) if history else "No previous requests."

    user_message = f"""Purchase request details:
- Product: {parsed.get('product')}
- Quantity: {parsed.get('quantity')}
- Department: {department}
- Budget (VND): {parsed.get('budget_vnd')}
- Priority: {parsed.get('priority')}
- Deadline: {parsed.get('deadline_days')} days

Recent procurement history for this department:
{history_text}"""

    result = call_llm(RISK_PROMPT, user_message)
    if not result:
        return {"risk_result": {"risk_score": "unknown", "flags": [], "reasoning": "Risk analysis failed."}}
    return {"risk_result": result}
