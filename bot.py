import os
import telebot
from flask import Flask, request

BOT_TOKEN = os.environ.get('BOT_TOKEN')
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)
user_points = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! Use /add <number> to save points, or /balance to view them.")

@bot.message_handler(commands=['add'])
def add_points(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "Usage: /add 10")
            return
        amount = int(parts[1])
        uid = message.from_user.id
        user_points[uid] = user_points.get(uid, 0) + amount
        bot.reply_to(message, f"Added {amount} points. Total: {user_points[uid]}")
    except ValueError:
        bot.reply_to(message, "Please provide a valid number.")

@bot.message_handler(commands=['balance'])
def show_balance(message):
    uid = message.from_user.id
    bot.reply_to(message, f"Your current balance is: {user_points.get(uid, 0)} points.")

@app.route('/health')
def health():
    return "ok", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "ok", 200
    return "forbidden", 403

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
