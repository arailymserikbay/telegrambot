import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")

MODEL_NAME = os.getenv("MODEL_NAME", "llama3")
OLLAMA_URL = os.getenv("OLLAMA_URL")

MAX_CONTEXT_MESSAGES = int(os.getenv("MAX_CONTEXT_MESSAGES", 10))
MAX_IMAGE_MB = int(os.getenv("MAX_IMAGE_MB", 10))

DATA_DIR = "data/images"
