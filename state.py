from typing import TypedDict, Optional

class ProcurementState(TypedDict):
    user_input: str
    submitter: Optional[dict]
    parsed_request: Optional[dict]
    budget_result: Optional[dict]
    risk_result: Optional[dict]
    vendor_result: Optional[dict]
    routing_result: Optional[dict]
    notification_result: Optional[dict]
    error: Optional[str]
