import random
import logging
from app.bot_manager import bot, template_env, subscribers

logger = logging.getLogger(__name__)


async def broadcast_market_update() -> None:
    """Generates synthetic market data, renders the Jinja2 template, and broadcasts."""
    if not subscribers:
        logger.info("No subscribers available for broadcast.")
        return

    # Generate synthetic market data
    context_data = {
        "gold_price": round(random.uniform(2300.0, 2450.0), 2),
        "btc_price": round(random.uniform(59000.0, 63000.0), 2),
        "aapl_price": round(random.uniform(170.0, 195.0), 2),
        "trend": "UPWARD 🚀" if random.random() > 0.5 else "DOWNWARD 📉"
    }

    # Render template using Jinja2
    template = template_env.get_template("market_update.jinja2")
    rendered_message = template.render(**context_data)

    # Broadcast to all registered tenants/subscribers
    success_count = 0
    for chat_id in subscribers:
        try:
            await bot.send_message(chat_id=chat_id, text=rendered_message)
            success_count += 1
        except Exception as e:
            logger.error(f"Failed to send broadcast to {chat_id}: {str(e)}")
            
    logger.info(f"Broadcast completed. Sent to {success_count} clients.")