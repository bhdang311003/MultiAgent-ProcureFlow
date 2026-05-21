import json
from state import ProcurementState
from llm_client import call_llm
from mock_data import VENDOR_CATALOG

VENDOR_PROMPT = """You are a procurement specialist. Given a list of vendors and purchase requirements, return ONLY a valid JSON object:
{
  "recommended_vendor": "vendor name",
  "unit_price": <integer>,
  "total_price": <integer>,
  "reasoning": "brief explanation of why this vendor is best"
}
Consider: price, delivery time vs deadline, warranty."""


def run(state: ProcurementState) -> dict:
    parsed = state["parsed_request"]
    product = parsed.get("product")
    
    vendors = VENDOR_CATALOG.get(product)
    if not vendors:
        return {"vendor_result": {
            "recommended_vendor": None,
            "unit_price": None,
            "total_price": None,
            "reasoning": f"No vendor data found for '{product}'.",
        }}
    
    quantity = parsed.get("quantity") or 1
    deadline_days = parsed.get("deadline_days")

    user_message = f"""Product: {product}
Quantity needed: {quantity}
Deadline: {deadline_days} days

Available vendors:
{json.dumps(vendors, ensure_ascii=False, indent=2)}"""

    result = call_llm(VENDOR_PROMPT, user_message)
    if not result:
        return {"vendor_result": {"recommended_vendor": None, "reasoning": "Vendor comparison failed."}}
    return {"vendor_result": result}
