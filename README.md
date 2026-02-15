# Local AI Telegram Bot

A powerful Telegram bot that runs entirely on your local machine, using **Ollama** for LLM (Llama 3, Gemma, etc.) and **Salesforce BLIP** for image captioning.

## 🚀 Features

- **Local LLM Inference**: Chats with you using powerful open-source models (Llama 3 by default) via Ollama.
- **Computer Vision**: Analyzes images you send using the BLIP model to provide descriptions.
- **Privacy Focused**: All data processing handling happens locally on your machine.
- **Asynchronous Design**: Built with `aiohttp` and `asyncio` to handle multiple requests without freezing.

## 🛠 Prerequisites

1.  **Python 3.10+**
2.  **Ollama**: [Download and install Ollama](https://ollama.com).
3.  **Ngrok**: [Sign up and install Ngrok](https://ngrok.com) (for exposing the local webhook).

## 📥 Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd telegrambot
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Pull the LLM model**:
    ```bash
    ollama pull llama3
    ```

## ⚙️ Configuration

1.  Create a `.env` file in the root directory (copy from example if available):
    ```ini
    # Telegram Bot Token (from @BotFather)
    BOT_TOKEN=your_bot_token_here

    # Ngrok URL (will update this every time you restart ngrok)
    BASE_URL=https://your-ngrok-url.ngrok-free.app
    WEBHOOK_PATH=/telegram/webhook

    # AI Configuration
    MODEL_NAME=llama3
    # Optional: Custom Ollama URL (default: http://localhost:11434/api/chat)
    # OLLAMA_URL=http://localhost:11434/api/chat

    # Limits
    MAX_CONTEXT_MESSAGES=10
    MAX_IMAGE_MB=10
    ```

## 🏃‍♂️ Running the Bot

1.  **Start Ollama** (in a separate terminal):
    ```bash
    ollama serve
    ```

2.  **Start Ngrok** (in another terminal):
    ```bash
    ngrok http 8000
    ```
    *Copy the `https://...` URL provided by ngrok and update `BASE_URL` in your `.env` file.*

3.  **Start the Bot**:
    ```bash
    uvicorn app.main:app --reload
    ```
    *The bot will automatically set the webhook on startup.*

## 🐳 Docker Support

You can also run the bot using Docker Compose:

```bash
docker-compose up --build
```
*Note: You will still need to run Ngrok on your host machine and update the `.env` file with the correct URL. For Docker, ensure Ollama is accessible (e.g., using `host.docker.internal`).*

## 📝 Usage

- **/start**: Welcome message.
- **/reset**: Clear the conversation context (memory).
- **Text**: Chat with the Llama 3 model.
- **Image**: Send an image, and the bot will describe it using BLIP, then the LLM will answer any questions about it.

## 🛠 Troubleshooting

- **Bot not responding?**
  - Check if `ngrok` is running and `BASE_URL` in `.env` matches the ngrok URL.
  - Ensure `uvicorn` is running without errors.
- **Ollama connection error?**
  - Ensure `ollama serve` is running.
  - Verify the model name in `.env` matches what you pulled (`ollama list`).

## 📜 License

MIT
