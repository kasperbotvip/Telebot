import telebot
import yt_dlp
import os

BOT_TOKEN = "6188422479:AAEjeLAGKvXnPyrmA94VcPpuedvboKtZ5fE"
bot = telebot.TeleBot(BOT_TOKEN)

# أمر /start للترحيب
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 أهلاً أسامة، البوت شغال! \nاستخدم /yt لتنزيل الصوت من يوتيوب 🎶 أو /dl لتنزيل من أي موقع سوشيال ميديا 📥")

# أمر /yt لتحميل الصوت من يوتيوب
@bot.message_handler(commands=['yt'])
def download_audio(message):
    try:
        url = message.text.split(maxsplit=1)[1]  # الرابط بعد الأمر
    except IndexError:
        bot.reply_to(message, "اكتب الأمر هكذا:\n/yt رابط_يوتيوب")
        return

    bot.reply_to(message, "⏳ جاري التحميل من يوتيوب...")

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
            bot.send_audio(message.chat.id, f)

        os.remove(audio_file)

    except Exception as e:
        bot.reply_to(message, f"❌ صار خطأ: {e}")

# أمر /dl لتحميل من أي موقع سوشيال ميديا (TikTok, Instagram, Facebook, Twitter...)
@bot.message_handler(commands=['dl'])
def download_social_media(message):
    try:
        url = message.text.split(maxsplit=1)[1]
    except IndexError:
        bot.reply_to(message, "اكتب الأمر هكذا:\n/dl رابط_الميديا")
        return

    bot.reply_to(message, "⏳ جاري التحميل من الرابط...")

    ydl_opts = {
        'outtmpl': 'downloaded_media.%(ext)s',
        'format': 'best',
        'retries': 3,
        'nocheckcertificate': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        # إرسال الملف حسب نوعه
        with open(filename, "rb") as f:
            if filename.endswith((".mp3", ".m4a")):
                bot.send_audio(message.chat.id, f)
            elif filename.endswith((".mp4", ".webm")):
                bot.send_video(message.chat.id, f)
            else:
                bot.send_document(message.chat.id, f)

        os.remove(filename)

    except Exception as e:
        bot.reply_to(message, f"❌ فشل التحميل: {e}")

if __name__ == "__main__":
    print("YouTube & Social Media Bot is running...")
    bot.infinity_polling()
