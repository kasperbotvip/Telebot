import telebot
import yt_dlp
import os

# ✅ التوكن الجديد
BOT_TOKEN = "5788330295:AAHhDVCjGt6g2vBrCuyAKK5Zjj3o73s7yTg"
bot = telebot.TeleBot(BOT_TOKEN)

pending_links = {}

def download_media(url, mode):
    # إعدادات التحميل حسب النوع
    ydl_opts = {
        "outtmpl": "audio.%(ext)s" if mode == "audio" else "video.%(ext)s",
        "format": "bestaudio/best" if mode == "audio" else "bestvideo+bestaudio/best",
        "merge_output_format": "mp4" if mode == "video" else None,
    }

    # ✅ استخدام ملف cookies.txt إذا موجود
    if os.path.exists("cookies.txt"):
        ydl_opts["cookies"] = "cookies.txt"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "👋 أرسل رابط يوتيوب أو أي موقع مدعوم، وبعدها اختر نوع التحميل.")

@bot.message_handler(func=lambda m: m.text and m.text.startswith("http"))
def handle_link(message):
    pending_links[message.from_user.id] = message.text.strip()
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🎬 فيديو", callback_data="video"))
    markup.add(telebot.types.InlineKeyboardButton("🎶 صوت", callback_data="audio"))
    bot.send_message(message.chat.id, "📥 اختر نوع التحميل:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["video", "audio"])
def process_download(call):
    url = pending_links.get(call.from_user.id)
    if not url:
        bot.send_message(call.message.chat.id, "❌ لم يتم العثور على رابط.")
        return

    bot.send_message(call.message.chat.id, "⏳ جاري التحميل...")
    try:
        file_path = download_media(url, call.data)
        if call.data == "video":
            bot.send_video(call.message.chat.id, open(file_path, "rb"))
        else:
            bot.send_audio(call.message.chat.id, open(file_path, "rb"))
        del pending_links[call.from_user.id]
    except Exception as e:
        bot.send_message(call.message.chat.id, f"❌ خطأ في التحميل:\n{e}")

bot.infinity_polling()
