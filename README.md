# Enterprise Telegram Bot with Jinja2 Templating

![Python](https://img.shields.io/badge/python-3.14-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688.svg?logo=fastapi)
![Telegram](https://img.shields.io/badge/Telegram-aiogram_3-2CA5E0.svg?logo=telegram)

An asynchronous Telegram broadcasting engine integrated directly within a **FastAPI** lifecycle. It utilizes **Jinja2** for dynamic HTML message rendering (supporting expandable blockquotes) and **APScheduler** for automated job execution.

## 🧠 Architecture Flow

```mermaid
graph TD
    A[FastAPI Lifespan] --> B[aiogram Long-Polling Task]
    A --> C[APScheduler Task]
    
    B -->|Client /start| D[(In-Memory Sub Set)]
    
    C -->|Every 1 Minute| E{Jinja2 Engine}
    E -->|Renders Data| F[templates/market_update.jinja2]
    F -->|HTML Payload| G[Telegram API]
    G -->|Broadcast| D
```

## 🚀 Quick Start (Docker)

1. Get a Bot Token from [@BotFather](https://t.me/BotFather).
2. Insert your token into `docker-compose.yml` under `TELEGRAM_BOT_TOKEN`.
3. Start the engine:
   ```bash
   docker compose up -d --build
   ```
4. Send `/start` to your bot in Telegram to subscribe.
5. Wait 60 seconds for the automated broadcast, or trigger it manually via the API:
   ```bash
   curl -X POST http://localhost:8099/v1/trigger-broadcast
   ```