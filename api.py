import json
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langgraph.types import Command

from graph import workflow
from state import ProcurementState
from memory import save_request, add_active_request, remove_active_request, load_active_requests

app = FastAPI(title="Procurement Approval System")


class SubmitRequest(BaseModel):
    user_input: str
    submitter_name: str
    submitter_email: str


class DecisionRequest(BaseModel):
    decision: str  # "approve" or "reject"


def _get_pending_interrupt(config: dict):
    """Lấy thông tin approver đang chờ từ interrupt hiện tại."""
    state = workflow.get_state(config)
    if state.tasks and state.tasks[0].interrupts:
        return state.tasks[0].interrupts[0].value
    return None


@app.get("/requests")
def list_requests():
    return load_active_requests()


@app.get("/requests/{thread_id}")
def get_request(thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    state = workflow.get_state(config)

    if not state.values:
        raise HTTPException(status_code=404, detail="Request not found.")

    pending = _get_pending_interrupt(config)
    routing = state.values.get("routing_result") or {}

    return {
        "thread_id": thread_id,
        "status": routing.get("final_status", "pending_approval"),
        "waiting_for": pending,
        "parsed_request": state.values.get("parsed_request"),
        "budget_result": state.values.get("budget_result"),
        "risk_result": state.values.get("risk_result"),
        "vendor_result": state.values.get("vendor_result"),
        "routing_result": routing,
    }


@app.post("/requests/{thread_id}/decision")
def submit_decision(thread_id: str, body: DecisionRequest):
    if body.decision not in ("approve", "reject"):
        raise HTTPException(status_code=400, detail="Decision must be 'approve' or 'reject'.")

    config = {"configurable": {"thread_id": thread_id}}

    if not _get_pending_interrupt(config):
        raise HTTPException(status_code=400, detail="No pending approval for this request.")

    workflow.invoke(Command(resume=body.decision), config=config)

    pending = _get_pending_interrupt(config)
    final_state = workflow.get_state(config).values
    routing = final_state.get("routing_result") or {}
    final_status = routing.get("final_status")

    # Workflow kết thúc — lưu vào history và xóa khỏi active
    if not pending and final_status:
        save_request(final_state.get("parsed_request") or {}, final_status)
        remove_active_request(thread_id)

    return {
        "thread_id": thread_id,
        "status": final_status or "pending_approval",
        "waiting_for": pending,
    }


@app.post("/requests")
def submit_request(body: SubmitRequest):
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    initial_state: ProcurementState = {
        "user_input": body.user_input,
        "submitter": {"name": body.submitter_name, "email": body.submitter_email},
        "parsed_request": None,
        "budget_result": None,
        "risk_result": None,
        "vendor_result": None,
        "routing_result": None,
        "notification_result": None,
        "error": None,
    }

    workflow.invoke(initial_state, config=config)

    state = workflow.get_state(config).values
    product = (state.get("parsed_request") or {}).get("product", "Unknown")
    add_active_request(thread_id, product)

    pending = _get_pending_interrupt(config)
    return {
        "thread_id": thread_id,
        "status": "pending_approval",
        "waiting_for": pending,
    }
