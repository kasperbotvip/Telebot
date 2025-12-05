import telebot
from youtube_downloader import download_media
from social_manager import post_to_social

BOT_TOKEN = "5788330295:AAHhDVCjGt6g2vBrCuyAKK5Zjj3o73s7yTg"
bot = telebot.TeleBot(BOT_TOKEN)

pending_links = {}
pending_files = {}

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
        pending_files[call.from_user.id] = file_path

        markup = telebot.types.InlineKeyboardMarkup()
        for p in ["instagram", "facebook", "twitter", "tiktok", "youtube", "telegram"]:
            markup.add(telebot.types.InlineKeyboardButton(p.capitalize(), callback_data=f"post_{p}"))
        bot.send_message(call.message.chat.id, "🌐 اختر المنصة للنشر:", reply_markup=markup)

    except Exception as e:
        err = str(e)

        # رسالة مفهومة إذا المشكلة تحقق-دخول يوتيوب
        if "Sign in to confirm you’re not a bot" in err or "Sign in to confirm" in err:
            bot.send_message(
                call.message.chat.id,
                "⚠️ يوتيوب يطلب تسجيل دخول لهذا الرابط. رجاءً تأكد من وجود ملف cookies.txt صالح ومحدّث بجانب التطبيق."
            )
        else:
            bot.send_message(call.message.chat.id, f"❌ خطأ في التحميل:\n{err}")

@bot.callback_query_handler(func=lambda call: call.data.startswith("post_"))
def process_post(call):
    platform = call.data.replace("post_", "")
    file_path = pending_files.get(call.from_user.id)
    if not file_path:
        bot.send_message(call.message.chat.id, "❌ لا يوجد ملف جاهز.")
        return

    result = post_to_social(file_path, platform)
    bot.send_message(call.message.chat.id, result)
    del pending_files[call.from_user.id]

bot.infinity_polling()
