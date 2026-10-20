import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Simple in-memory storage for demonstration (resets on restart)
user_rewards = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        f"Hi {user.first_name}! Welcome to the AdRewards Bot.\n"
        "Use /reward to claim your test reward point."
    )

async def reward(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Simple function: Increment reward counter for the user."""
    user_id = update.effective_user.id
    
    # Initialize or increment
    if user_id not in user_rewards:
        user_rewards[user_id] = 0
    user_rewards[user_id] += 1
    
    current_total = user_rewards[user_id]
    
    await update.message.reply_text(
        f"✅ Reward claimed! You have earned {current_total} test point(s)."
    )

def main() -> None:
    """Start the bot."""
    # Railway uses environment variables for secrets
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("No TELEGRAM_BOT_TOKEN found in environment variables.")

    application = Application.builder().token(token).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("reward", reward))

    # Run the bot (Long Polling - ideal for Railway worker)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
