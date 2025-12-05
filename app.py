import telebot
import yt_dlp
import os

BOT_TOKEN = "6188422479:AAEjeLAGKvXnPyrmA94VcPpuedvboKtZ5fE"
ADMIN_ID = 988757303
bot = telebot.TeleBot(BOT_TOKEN)

users = set()
pending_links = {}  # تخزين الرابط لكل مستخدم

# دالة التحميل
def download_media(url, mode):
    if mode == "audio":
        output = "audio.%(ext)s"
        ydl_opts = {
            "outtmpl": output,
            "format": "bestaudio/best",
            "cookies": "cookies.txt" if os.path.exists("cookies.txt") else None
        }
    else:  # video
        output = "video.%(ext)s"
        ydl_opts = {
            "outtmpl": output,
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "cookies": "cookies.txt" if os.path.exists("cookies.txt") else None
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# استقبال أي رابط
@bot.message_handler(func=lambda m: m.text and m.text.startswith("http"))
def handle_link(message):
    users.add(message.from_user.id)
    url = message.text.strip()
    pending_links[message.from_user.id] = url

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🎬 فيديو", callback_data="video"))
    markup.add(telebot.types.InlineKeyboardButton("🎶 صوت", callback_data="audio"))
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
        file_path = download_media(url, call.data)

        if call.data == "video":
            bot.send_video(call.message.chat.id, open(file_path, "rb"))
        else:
            bot.send_audio(call.message.chat.id, open(file_path, "rb"))

        del pending_links[user_id]

    except Exception as e:
        bot.send_message(call.message.chat.id, f"❌ خطأ في التحميل:\n{e}")

# أمر /start للترحيب
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "👋 أرسل رابط (يوتيوب أو أي موقع مدعوم) وسيتم تخييرك بين تحميل فيديو أو صوت.")

bot.infinity_polling()
