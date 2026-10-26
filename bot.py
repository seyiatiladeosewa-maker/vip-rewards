import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Replace with your actual token from BotFather
TOKEN = "YOUR_BOT_TOKEN_HERE"

# Simple in-memory storage (resets on restart; fine for a demo bot)
user_balances = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_balances:
        user_balances[user_id] = 0
    
    keyboard = [[InlineKeyboardButton("Claim Daily Bonus (+10)", callback_data='claim')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        f"Welcome to Rewards!\n\n"
        f"Your current balance: {user_balances[user_id]} points.\n"
        f"Click below to claim your daily bonus."
    )
    await update.message.reply_text(text, reply_markup=reply_markup)

async def claim_bonus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    # Simple logic: Add 10 points every time (In production, add a 24h timer)
    user_balances[user_id] = user_balances.get(user_id, 0) + 10
    
    await query.edit_message_text(
        text=f"Bonus claimed! Your new balance is {user_balances[user_id]} points.\n"
             f"(This is a demo. No real rewards are issued.)"
    )

def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(claim_bonus, pattern='claim'))
    
    # For Railway deployment, use polling (simple) or webhook (better for scale)
    app.run_polling()

if __name__ == '__main__':
    main()
