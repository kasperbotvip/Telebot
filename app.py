import telebot
import yt_dlp
import os

BOT_TOKEN = "6188422479:AAEjeLAGKvXnPyrmA94VcPpuedvboKtZ5fE"
bot = telebot.TeleBot(BOT_TOKEN)

# أمر /start للترحيب
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "👋 أهلاً أسامة، أرسل أي رابط من يوتيوب أو السوشيال ميديا، وأنا أعطيك خيارات التحميل 🎶🎬ℹ️")

# استقبال أي رابط
@bot.message_handler(func=lambda message: message.text.startswith("http"))
def ask_download_type(message):
    url = message.text.strip()
    try:
        # جلب معلومات الفيديو بدون تحميل
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
        title = info.get("title", "غير معروف")
        thumbnail = info.get("thumbnail", None)

        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(
            telebot.types.InlineKeyboardButton("🎶 حمل صوت", callback_data=f"audio|{url}"),
            telebot.types.InlineKeyboardButton("🎬 حمل فيديو", callback_data=f"video|{url}"),
            telebot.types.InlineKeyboardButton("ℹ️ معلومات", callback_data=f"info|{url}")
        )

        if thumbnail:
            bot.send_photo(message.chat.id, thumbnail, caption=f"📌 العنوان: {title}", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, f"📌 العنوان: {title}", reply_markup=markup)

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ خطأ في جلب المعلومات: {e}")

# التعامل مع الضغط على الأزرار
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    action, url = call.data.split("|", 1)
    bot.answer_callback_query(call.id)

    if action == "audio":
        bot.send_message(call.message.chat.id, "⏳ جاري التحميل كصوت...")
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloaded_audio.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                audio_file = filename.rsplit('.', 1)[0] + ".mp3"

            with open(audio_file, "rb") as f:
                bot.send_audio(call.message.chat.id, f)

            os.remove(audio_file)
        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ خطأ: {e}")

    elif action == "video":
        bot.send_message(call.message.chat.id, "⏳ جاري التحميل كفيديو...")
        ydl_opts = {
            'outtmpl': 'downloaded_video.%(ext)s',
            'format': 'best',
            'retries': 3,
            'nocheckcertificate': True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            with open(filename, "rb") as f:
                bot.send_video(call.message.chat.id, f)

            os.remove(filename)
        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ خطأ: {e}")

    elif action == "info":
        bot.send_message(call.message.chat.id, "🔍 جاري جلب المعلومات...")
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
            title = info.get("title", "غير معروف")
            duration = info.get("duration", 0)
            filesize = info.get("filesize", 0)
            bot.send_message(
                call.message.chat.id,
                f"ℹ️ معلومات الفيديو:\n\n📌 العنوان: {title}\n⏱️ المدة: {duration} ثانية\n💾 الحجم: {filesize/1024/1024:.2f} MB"
            )
        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ خطأ في جلب المعلومات: {e}")

if __name__ == "__main__":
    print("Bot with audio/video/info choice + thumbnail is running...")
    bot.infinity_polling()
