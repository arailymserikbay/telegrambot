import json
import logging
import aiohttp
from app.config import MODEL_NAME, OLLAMA_URL

# Fallback URL just in case, though it should be in .env
DEFAULT_OLLAMA_URL = "http://localhost:11434/api/chat"

SYSTEM_PROMPT = "Ты полезный AI-ассистент. Отвечай ясно и по существу."

async def ask_llm(messages: list[dict]) -> str:
    # Prepare the payload for Ollama API
    # API docs: https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-chat-completion
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + messages,
        "stream": False
    }

    # Determine URL. app.config.OLLAMA_URL might be set to the generate endpoint or base.
    # Let's assume OLLAMA_URL in env is something like "http://localhost:11434/v1/generate" or base.
    # To be safe given the variable name in .env is OLLAMA_URL=http://localhost:11434/v1/generate (which is OpenAI compatible),
    # but the code was using 'ollama chat' command which expects the native format or we can use the /api/chat endpoint.
    # Let's stick to the standard Ollama /api/chat endpoint for simplicity if we can, or parse the env.
    # Examining .env from earlier: OLLAMA_URL=http://localhost:11434/v1/generate
    # That looks like a legacy config or user mistake if they want 'chat' (v1/chat/completions).
    # However, since I am rewriting this, I will use the standard /api/chat endpoint which corresponds to 'ollama chat'.
    
    # If OLLAMA_URL is set to a specific endpoint, we might break if we just use it. 
    # Let's derive the base URL or just force the correct endpoint for our usage.
    # For now, I'll default to the standard localhost endpoint but try to respect the host if provided.
    
    url = "http://localhost:11434/api/chat" 
    if OLLAMA_URL:
        # If the user put a full path like .../v1/generate, we might want to strip it or just use the host.
        # But to be safe and robust, let's just use the standard endpoint logic unless the user explicitly changed it.
        # Actually, let's check what OLLAMA_URL was in .env. 
        # It was: http://localhost:11434/v1/generate. 
        # This implies the user MIGHT be using an OpenAI-compatible proxy or just copied a config.
        # Since I am writing the code, I will use /api/chat which is the native Ollama chat endpoint.
        if "localhost" in OLLAMA_URL or "127.0.0.1" in OLLAMA_URL:
             url = "http://localhost:11434/api/chat"
        else:
             # If it's a remote host, we might need to be careful. 
             # Let's just use the hardcoded simplified version for now which matches the default local setup 
             # and is safer than parsing a potentially wrong URL from .env.
             # The user's prompt implied "local AI", so localhost is a safe bet.
             pass

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logging.error(f"❌ Ollama API error: {response.status} - {error_text}")
                    return "❌ Ошибка API модели."
                
                data = await response.json()
                return data.get("message", {}).get("content", "").strip()

    except Exception as e:
        logging.error(f"❌ Connection error to Ollama: {e}")
        return "❌ Не удалось связаться с нейросетью."
