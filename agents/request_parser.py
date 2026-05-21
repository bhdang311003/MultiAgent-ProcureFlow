from state import ProcurementState
from llm_client import call_llm

PROMPT = """You are an AI that extracts structured information from internal procurement requests.
Return ONLY a valid JSON object with no extra text:
{
  "product": "product name",
  "quantity": <integer>,
  "department": "department name",
  "budget_vnd": <integer in VND>,
  "priority": "low" | "medium" | "high" | "urgent",
  "deadline_days": <integer, number of days until needed>
}
If a field is not mentioned in the request, use null."""


def run(state: ProcurementState) -> dict:
    result = call_llm(PROMPT, state["user_input"])
    if not result:
        return {"parsed_request": None, "error": "Failed to parse procurement request."}
    return {"parsed_request": result, "error": None}
