import telebot
from collections import Counter
import yt_dlp
import os

BOT_TOKEN = "6188422479:AAEjeLAGKvXnPyrmA94VcPpuedvboKtZ5fE"
ADMIN_ID = 988757303
bot = telebot.TeleBot(BOT_TOKEN)

users = set()
download_count = 0
downloaded_links = []
pending_links = {}  # user_id: link

# دالة تحميل من يوتيوب
def download_youtube(url, output):
    ydl_opts = {
        "outtmpl": output,
        "format": "bestaudio" if output.endswith(".mp3") else "best",
        "cookies": "cookies.txt" if os.path.exists("cookies.txt") else None
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output

# عند دخول المستخدم
@bot.message_handler(commands=['start'])
def welcome(message):
    users.add(message.from_user.id)
    bot.send_message(message.chat.id, "👋 أرسل رابط يوتيوب للتحميل.")

# استقبال الروابط
@bot.message_handler(func=lambda m: m.text and "youtube.com" in m.text or "youtu.be" in m.text)
def handle_link(message):
    users.add(message.from_user.id)
    pending_links[message.from_user.id] = message.text.strip()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🎬 حمل فيديو", callback_data="video"))
    markup.add(telebot.types.InlineKeyboardButton("🎶 حمل صوت", callback_data="audio"))
    bot.send_message(message.chat.id, "📥 اختر نوع التحميل:", reply_markup=markup)

# التعامل مع اختيار نوع التحميل
@bot.callback_query_handler(func=lambda call: call.data in ["video", "audio"])
def process_download(call):
    user_id = call.from_user.id
    url = pending_links.get(user_id)

    if not url:
        bot.send_message(call.message.chat.id, "❌ لم يتم العثور على رابط.")
        return

    bot.send_message(call.message.chat.id, "⏳ جاري التحميل...")

    try:
        if call.data == "video":
            file_path = download_youtube(url, "video.mp4")
            bot.send_video(call.message.chat.id, open(file_path, "rb"))
        else:
            file_path = download_youtube(url, "audio.mp3")
            bot.send_audio(call.message.chat.id, open(file_path, "rb"))

        download_count += 1
        downloaded_links.append(url)
        del pending_links[user_id]

    except Exception as e:
        bot.send_message(call.message.chat.id, f"❌ خطأ في التحميل:\n{e}")

bot.infinity_polling()
