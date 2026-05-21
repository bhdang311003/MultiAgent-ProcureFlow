from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from state import ProcurementState
from agents import (
    request_parser, budget_validator, risk_detector,
    vendor_comparator, approval_router,
    notify_approvers, human_approval, notify_submitter,
)


def _after_parse(state: ProcurementState) -> str:
    """Dừng sớm nếu LLM không parse được request."""
    return "validate_budget" if state["parsed_request"] else END


builder = StateGraph(ProcurementState)

builder.add_node("parse_request",     request_parser.run)
builder.add_node("validate_budget",   budget_validator.run)
builder.add_node("detect_risk",       risk_detector.run)
builder.add_node("compare_vendors",   vendor_comparator.run)
builder.add_node("route_approval",    approval_router.run)
builder.add_node("notify_approvers",  notify_approvers.run)
builder.add_node("human_approval",    human_approval.run)
builder.add_node("notify_submitter",  notify_submitter.run)

builder.set_entry_point("parse_request")
builder.add_conditional_edges("parse_request", _after_parse)
builder.add_edge("validate_budget",  "detect_risk")
builder.add_edge("detect_risk",      "compare_vendors")
builder.add_edge("compare_vendors",  "route_approval")
builder.add_edge("route_approval",   "notify_approvers")
builder.add_edge("notify_approvers", "human_approval")
builder.add_edge("human_approval",   "notify_submitter")
builder.add_edge("notify_submitter", END)

checkpointer = MemorySaver()
workflow = builder.compile(checkpointer=checkpointer)
