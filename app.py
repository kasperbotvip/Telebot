import telebot
import yt_dlp
import os

BOT_TOKEN = "6188422479:AAEjeLAGKvXnPyrmA94VcPpuedvboKtZ5fE"
bot = telebot.TeleBot(BOT_TOKEN)

# أمر /start للترحيب
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 أهلاً أسامة، البوت شغال! ارسل /yt مع رابط يوتيوب لتنزيل الصوت 🎶")

# أمر /yt لتحميل الصوت من يوتيوب
@bot.message_handler(commands=['yt'])
def download_audio(message):
    try:
        url = message.text.split(maxsplit=1)[1]  # الرابط بعد الأمر
    except IndexError:
        bot.reply_to(message, "اكتب الأمر هكذا:\n/yt رابط_يوتيوب")
        return

    bot.reply_to(message, "⏳ جاري التحميل...")

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
            audio_file = filename.replace(".webm", ".mp3").replace(".m4a", ".mp3")

        with open(audio_file, "rb") as f:
            bot.send_audio(message.chat.id, f)

        os.remove(audio_file)

    except Exception as e:
        bot.reply_to(message, f"❌ صار خطأ: {e}")

if __name__ == "__main__":
    print("YouTube Audio Bot is running...")
    bot.infinity_polling()
