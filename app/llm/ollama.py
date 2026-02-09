import requests
from app.config import MODEL_NAME, OLLAMA_URL

SYSTEM_PROMPT = "Ты полезный AI-ассистент. Отвечай ясно и по существу."

def ask_llm(messages: list[str]) -> str:
    prompt = SYSTEM_PROMPT + "\n\n"
    for m in messages:
        prompt += f"{m['role']}: {m['content']}\n"

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=60
    )
    response.raise_for_status()

    return response.json().get("response", "")
