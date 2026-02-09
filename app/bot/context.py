from collections import deque
from app.config import MAX_CONTEXT_MESSAGES

_context = {}

def get_context(chat_id: int):
    if chat_id not in _context:
        _context[chat_id] = deque(maxlen=MAX_CONTEXT_MESSAGES)
    return _context[chat_id]

def add_message(chat_id: int, role: str, content: str):
    ctx = get_context(chat_id)
    ctx.append({"role": role, "content": content})

def reset_context(chat_id: int):
    _context.pop(chat_id, None)
