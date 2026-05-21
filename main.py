import json
import uuid
from langgraph.types import Command
from graph import workflow
from state import ProcurementState
from memory import save_request

if __name__ == "__main__":
    user_input = """
    Cần mua 20 MacBook Pro M4 cho team AI Engineering, ngân sách khoảng 1 tỷ VNĐ, cần trong vòng 2 tuần."""

    initial_state: ProcurementState = {
        "user_input": user_input,
        "submitter": {"name": "Tran Van Y", "email": "y@company.com"},
        "parsed_request": None,
        "budget_result": None,
        "risk_result": None,
        "vendor_result": None,
        "routing_result": None,
        "notification_result": None,
        "error": None,
    }

    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    print(f"Request ID: {thread_id}\n")
    print(f"Input: {user_input}\n")

    # Chạy graph lần đầu — sẽ dừng tại human_approval
    result = workflow.invoke(initial_state, config=config)

    # Xử lý từng interrupt (mỗi approver một lần)
    while workflow.get_state(config).tasks and workflow.get_state(config).tasks[0].interrupts:
        # Lấy thông tin approver đang chờ từ interrupt
        pending = workflow.get_state(config).tasks[0].interrupts[0].value
        print(f"\n[Waiting for workflowroval]")
        print(f"  Approver : {pending['workflowrover']} ({pending['email']})")
        print(f"  Request  : {pending['request']}")

        decision = input("  Decision (workflowrove/reject): ").strip().lower()
        while decision not in ("workflowrove", "reject"):
            decision = input("  Invalid. Enter workflowrove or reject: ").strip().lower()

        # Resume graph với quyết định của approver
        result = workflow.invoke(Command(resume=decision), config=config)

    print("\n--- Final Result ---")
    final_state = workflow.get_state(config).values
    print(json.dumps(final_state, ensure_ascii=False, indent=2))

    # Lưu vào lịch sử để các request sau dùng cho risk detection
    final_status = (final_state.get("routing_result") or {}).get("final_status", "unknown")
    save_request(final_state.get("parsed_request") or {}, final_status)
