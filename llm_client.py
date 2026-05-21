import json
import os
from typing import Optional
import requests # type: ignore
from dotenv import load_dotenv # type: ignore

load_dotenv()

OPENROUTER_API_KEY = os.getenv("API_KEY")
model_LLM = "openai/gpt-oss-120b:free"


def call_llm(system_prompt: str, user_message: str) -> Optional[dict]:
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": model_LLM,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            "temperature": 0,
        })
    )
    data = response.json()
    if "error" in data:
        print("LLM error:", data["error"]["message"])
        return None

    content = data["choices"][0]["message"]["content"]
    if not content:
        print("LLM returned empty response")
        return None

    return json.loads(content)
