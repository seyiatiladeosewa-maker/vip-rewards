import os
import telebot
from dotenv import load_dotenv

load_dotenv()

# Use Environment Variable for security
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Simple reward function
    user_id = message.from_user.id
    # Generate a simple pseudo-unique reward code based on user ID
    reward_code = f"REWARD-{user_id % 10000:04d}"

    welcome_text = (
        f"🎉 **Welcome {message.from_user.first_name}!**\n\n"
        f"Here is your exclusive reward code: `{reward_code}`\n\n"
        f"Use this code at checkout for your benefit. Need a new code later? Just /start again."
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Simply send /start to get your reward code. That's it!")

# Echo fallback (optional but keeps engagement)
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Please type /start to get your reward code!")

if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()
