import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.title("Procurement Request System")
st.subheader("Submit a Purchase Request")

with st.form("request_form"):
    user_input = st.text_area(
        "Describe your purchase request",
        placeholder="e.g. Cần mua 20 MacBook Pro M4 cho team AI Engineering, ngân sách 1 tỷ VNĐ, cần trong 2 tuần.",
        height=120,
    )
    submitter_name = st.text_input("Your name")
    submitter_email = st.text_input("Your email")
    submitted = st.form_submit_button("Submit Request")

if submitted:
    if not user_input or not submitter_name or not submitter_email:
        st.error("Please fill in all fields.")
    else:
        with st.spinner("Processing your request..."):
            response = requests.post(f"{API_URL}/requests", json={
                "user_input": user_input,
                "submitter_name": submitter_name,
                "submitter_email": submitter_email,
            })

        if response.status_code == 200:
            data = response.json()
            st.success(f"Request submitted successfully!")
            st.info(f"Your Request ID: **{data['thread_id']}**")

            waiting = data.get("waiting_for")
            if waiting:
                st.warning(f"Waiting for approval from: **{waiting['approver']}** ({waiting['email']})")
        else:
            st.error(f"Error: {response.json().get('detail')}")

st.divider()
st.subheader("Request Status")

active_list = requests.get(f"{API_URL}/requests").json()
if active_list:
    for item in active_list:
        if st.button(f"{item['product']} — {item['thread_id']}", key=item["thread_id"]):
            r = requests.get(f"{API_URL}/requests/{item['thread_id']}")
            if r.status_code == 200:
                data = r.json()
                status = data.get("status", "unknown")
                if status == "approved":
                    st.success(f"{item['product']}: APPROVED")
                elif status == "rejected":
                    st.error(f"{item['product']}: REJECTED")
                else:
                    waiting = data.get("waiting_for")
                    if waiting:
                        st.warning(f"Pending approval from: **{waiting['approver']}** ({waiting['email']})")
                with st.expander("View full details"):
                    st.json(data)
else:
    st.info("No active requests.")
