import os
import streamlit as st
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.title("Approver Portal")
st.subheader("Review and Approve Purchase Requests")

# Danh sách request đang pending
pending_list = requests.get(f"{API_URL}/requests").json()
if pending_list:
    st.markdown("**Pending Requests:**")
    for item in pending_list:
        if st.button(f"{item['product']} — {item['thread_id']}", key=item["thread_id"]):
            r = requests.get(f"{API_URL}/requests/{item['thread_id']}")
            if r.status_code == 200:
                st.session_state["request_data"] = r.json()
                st.session_state["thread_id"] = item["thread_id"]
                st.rerun()
else:
    st.info("No pending requests.")

st.divider()

def row(label, value):
    c1, c2 = st.columns([1, 2])
    c1.markdown(f"**{label}**")
    c2.write(value)

if "request_data" in st.session_state:
    data = st.session_state["request_data"]
    id = data.get("thread_id") or {}
    parsed = data.get("parsed_request") or {}
    risk = data.get("risk_result") or {}
    vendor = data.get("vendor_result") or {}
    budget = data.get("budget_result") or {}
    status = data.get("status", "unknown")

    budget_vnd = parsed.get("budget_vnd")
    risk_score = risk.get("risk_score", "unknown")

    row("Request ID", f"{id}")
    row("Product", f"{parsed.get('quantity')}x {parsed.get('product')}")
    row("Department", parsed.get("department"))
    row("Budget Requested", f"{budget_vnd:,} VND" if budget_vnd else "N/A")
    row("Deadline", f"{parsed.get('deadline_days')} days")
    row("Budget Status", "Sufficient" if budget.get("approved") else "Exceeded")
    row("Recommended Vendor", vendor.get("recommended_vendor") or "No vendor found")
    row("Vendor Reasoning", vendor.get("reasoning") or "-")

    c1, c2 = st.columns([1, 2])
    c1.markdown("**Risk Score**")
    if risk_score == "high":
        c2.error("HIGH RISK")
    elif risk_score == "medium":
        c2.warning("MEDIUM RISK")
    else:
        c2.success("LOW RISK")

    if risk.get("flags"):
        st.warning("Risk Flags: " + ", ".join(risk.get("flags")))

    waiting = data.get("waiting_for")
    if waiting and status not in ("approved", "rejected"):
        st.divider()
        st.info(f"Waiting for: **{waiting['approver']}** ({waiting['email']})")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Approve", use_container_width=True):
                requests.post(
                    f"{API_URL}/requests/{st.session_state['thread_id']}/decision",
                    json={"decision": "approve"},
                )
                r = requests.get(f"{API_URL}/requests/{st.session_state['thread_id']}")
                if r.status_code == 200:
                    st.session_state["request_data"] = r.json()
                    st.rerun()
        with col2:
            if st.button("Reject", use_container_width=True):
                requests.post(
                    f"{API_URL}/requests/{st.session_state['thread_id']}/decision",
                    json={"decision": "reject"},
                )
                r = requests.get(f"{API_URL}/requests/{st.session_state['thread_id']}")
                if r.status_code == 200:
                    st.session_state["request_data"] = r.json()
                    st.rerun()
    elif status == "approved":
        st.success("This request has been APPROVED.")
    elif status == "rejected":
        st.error("This request has been REJECTED.")
