import telebot

# التوكن مال البوت
BOT_TOKEN = "6188422479:AAEjeLAGKvXnPyrmA94VcPpuedvboKtZ5fE"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً! البوت شغال ✅")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"انت كتبت: {message.text}")

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
