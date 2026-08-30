import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.bot_manager import dp, bot
from app.scheduler import broadcast_market_update

scheduler = AsyncIOScheduler()
polling_task: asyncio.Task | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global polling_task
    
    # 1. Start background job scheduler (Runs every 1 minute)
    scheduler.add_job(broadcast_market_update, 'interval', minutes=1)
    scheduler.start()
    
    # 2. Start Telegram bot long-polling as a background asyncio task
    if bot.token != "mock_token":
        polling_task = asyncio.create_task(dp.start_polling(bot))
    
    yield
    
    # 3. Graceful shutdown
    scheduler.shutdown()
    if polling_task:
        polling_task.cancel()


app = FastAPI(
    title="Telegram Broadcasting API",
    lifespan=lifespan
)


@app.post("/v1/trigger-broadcast", tags=["Manual Controls"])
async def trigger_manual_broadcast():
    """Provides a REST endpoint to forcefully trigger the broadcast job immediately."""
    await broadcast_market_update()
    return {"status": "success", "message": "Manual broadcast triggered successfully."}