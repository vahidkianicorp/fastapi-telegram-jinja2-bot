import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "mock_token")

# Initialize bot with HTML parse mode for Jinja2 rendering compatibility
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Load Jinja2 templates directory
template_env = Environment(loader=FileSystemLoader("app/templates"))

# In-memory set to track subscribers (In production, use PostgreSQL/SQLite)
subscribers: set[int] = set()


@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    """Registers user chat ID to receive automated broadcasts."""
    chat_id = message.chat.id
    subscribers.add(chat_id)
    
    welcome_text = (
        "✅ <b>Successfully Subscribed!</b>\n\n"
        "You will now receive scheduled market updates rendered dynamically via Jinja2."
    )
    await message.answer(welcome_text)
    logger.info(f"New subscriber added: {chat_id}")