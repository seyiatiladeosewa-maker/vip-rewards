import telebot
import os

# Initialize bot with token from Railway Environment Variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# In-memory storage (resets on restart; sufficient for a simple tool)
user_points = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Use /add <number> to save points, or /balance to view them.")

@bot.message_handler(commands=['add'])
def add_points(message):
    try:
        # Extract the number from the command
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "Usage: /add 10")
            return
        
        amount = int(parts[1])
        user_id = message.from_user.id
        
        if user_id not in user_points:
            user_points[user_id] = 0
            
        user_points[user_id] += amount
        bot.reply_to(message, f"Added {amount} points. Total: {user_points[user_id]}")
        
    except ValueError:
        bot.reply_to(message, "Please provide a valid number.")

@bot.message_handler(commands=['balance'])
def show_balance(message):
    user_id = message.from_user.id
    points = user_points.get(user_id, 0)
    bot.reply_to(message, f"Your current balance is: {points} points.")

# Start polling
bot.infinity_polling()
