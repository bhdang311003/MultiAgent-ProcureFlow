from state import ProcurementState
from mock_data import APPROVERS, THRESHOLDS
from llm_client import call_llm

CLASSIFY_PROMPT = """You are a procurement policy expert. Given a product name, determine if it requires special executive approval.
Return ONLY a valid JSON object:
{
  "sensitive": true | false,
  "reason": "brief reason why or why not"
}
A product is sensitive if it involves: infrastructure, security, large-scale IT systems, regulated industries, or strategic assets."""


def _classify_product(product: str) -> dict:
    result = call_llm(CLASSIFY_PROMPT, f"Product: {product}")
    return result or {"sensitive": False, "reason": "Classification failed, defaulting to non-sensitive."}


def run(state: ProcurementState) -> dict:
    parsed = state["parsed_request"]
    amount = parsed.get("budget_vnd") or 0
    priority = parsed.get("priority") or "medium"
    product = parsed.get("product") or ""
    budget_ok = state["budget_result"].get("approved", False)
    risk_score = (state["risk_result"] or {}).get("risk_score", "low")

    reasons = []

    # Base chain theo số tiền
    if not budget_ok:
        chain = ["manager", "finance"]
        reasons.append("budget exceeded")
    elif amount < THRESHOLDS["manager_only"]:
        chain = ["manager"]
        reasons.append("standard amount")
    elif amount < THRESHOLDS["finance_required"]:
        chain = ["manager", "finance"]
        reasons.append("mid-range amount")
    else:
        chain = ["manager", "finance", "cto"]
        reasons.append("high-value amount")

    # Risk cao → kéo CTO vào nếu chưa có
    if risk_score == "high" and "cto" not in chain:
        chain.append("cto")
        reasons.append("high risk")

    # LLM phân loại sản phẩm nhạy cảm → kéo CTO vào
    classification = _classify_product(product)
    if classification.get("sensitive") and "cto" not in chain:
        chain.append("cto")
        reasons.append(f"sensitive product: {classification.get('reason')}")

    # Urgent + budget ok + chưa cần CTO → bỏ finance để duyệt nhanh
    if priority == "urgent" and budget_ok and "finance" in chain and "cto" not in chain:
        chain.remove("finance")
        reasons.append("urgent — finance bypassed")

    return {"routing_result": {
        "approval_chain": chain,
        "approvers": [APPROVERS[a] for a in chain],
        "reason": ", ".join(reasons),
        "status": "pending_approval",
        "product_classification": classification,
    }}
