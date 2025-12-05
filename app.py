import telebot
from youtube_downloader import download_youtube
from social_downloader import download_social
import os

BOT_TOKEN = "ضع_التوكن_هنا"
bot = telebot.TeleBot(BOT_TOKEN)

pending_links = {}

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "👋 أرسل رابط مباشر (يوتيوب أو أي موقع سوشيال ميديا مدعوم).")

@bot.message_handler(func=lambda m: m.text and m.text.startswith("http"))
def handle_link(message):
    url = message.text.strip()
    pending_links[message.from_user.id] = url

    # تحديد نوع الرابط (يوتيوب أو سوشيال)
    if "youtube.com" in url or "youtu.be" in url:
        source = "youtube"
    else:
        source = "social"

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🎬 فيديو", callback_data=f"{source}_video"))
    markup.add(telebot.types.InlineKeyboardButton("🎶 صوت", callback_data=f"{source}_audio"))
    bot.send_message(message.chat.id, f"📥 اختر نوع التحميل ({source}):", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.endswith(("video","audio")))
def process_download(call):
    url = pending_links.get(call.from_user.id)
    if not url:
        bot.send_message(call.message.chat.id, "❌ لم يتم العثور على رابط.")
        return

    bot.send_message(call.message.chat.id, "⏳ جاري التحميل...")
    try:
        source, mode = call.data.split("_")

        if source == "youtube":
            file_path = download_youtube(url, mode)
        else:
            file_path = download_social(url, mode)

        if mode == "video":
            with open(file_path, "rb") as f:
                bot.send_video(call.message.chat.id, f)
        else:
            with open(file_path, "rb") as f:
                bot.send_audio(call.message.chat.id, f)

        del pending_links[call.from_user.id]

    except Exception as e:
        bot.send_message(call.message.chat.id, f"❌ خطأ في التحميل:\n{e}")

bot.infinity_polling()
