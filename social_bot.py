import telebot
import yt_dlp
import os

BOT_TOKEN = "ضع_التوكن_هنا"
bot = telebot.TeleBot(BOT_TOKEN)

pending_links = {}

# ✅ دالة التحميل من روابط السوشيال ميديا
def download_social(url, mode):
    ydl_opts = {
        "noplaylist": True,
        "geo_bypass": True,
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
    }

    if mode == "audio":
        ydl_opts.update({
            "format": "bestaudio/best",
            "outtmpl": "social_audio.%(ext)s",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "m4a",
                    "preferredquality": "192",
                }
            ],
        })
    else:
        ydl_opts.update({
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "outtmpl": "social_video.%(ext)s",
        })

    if os.path.exists("cookies.txt"):
        ydl_opts["cookiefile"] = "cookies.txt"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filepath = ydl.prepare_filename(info)

        if mode == "audio":
            base = os.path.splitext(filepath)[0]
            m4a_path = base + ".m4a"
            mp3_path = base + ".mp3"
            if os.path.exists(m4a_path):
                return m4a_path
            if os.path.exists(mp3_path):
                return mp3_path

        return filepath

# ✅ أوامر البوت
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "👋 أرسل رابط مباشر من أي موقع سوشيال ميديا (تيك توك، فيسبوك، إنستغرام...).")

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
        file_path = download_social(url, call.data)

        if call.data == "video":
            with open(file_path, "rb") as f:
                bot.send_video(call.message.chat.id, f)
        else:
            with open(file_path, "rb") as f:
                bot.send_audio(call.message.chat.id, f)

        del pending_links[call.from_user.id]

    except Exception as e:
        bot.send_message(call.message.chat.id, f"❌ خطأ في التحميل:\n{e}")

bot.infinity_polling()
