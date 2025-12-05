import telebot
from collections import Counter
import yt_dlp
import os

# ✅ التوكن الخاص بالبوت
BOT_TOKEN = "6188422479:AAEjeLAGKvXnPyrmA94VcPpuedvboKtZ5fE"
ADMIN_ID = 988757303
bot = telebot.TeleBot(BOT_TOKEN)

# تخزين المستخدمين والتحميلات
users = set()
download_count = 0
downloaded_links = []

# ✅ دالة تحميل من يوتيوب باستخدام yt-dlp
def download_youtube(url, output="downloaded.mp4"):
    ydl_opts = {
        "outtmpl": output,
        "format": "best",
        # إذا عندك ملف cookies.txt مرفوع على السيرفر
        "cookies": "cookies.txt" if os.path.exists("cookies.txt") else None
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output

# أول رسالة عند دخول أي مستخدم
@bot.message_handler(commands=['start'])
def welcome(message):
    users.add(message.from_user.id)

    if message.from_user.id == ADMIN_ID:
        # لوحة الأدمن تظهر مباشرة
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("➕ إضافة قناة", callback_data="add_channel"))
        markup.add(telebot.types.InlineKeyboardButton("❌ حذف قناة", callback_data="del_channel"))
        markup.add(telebot.types.InlineKeyboardButton("📋 عرض القنوات", callback_data="list_channels"))
        markup.add(telebot.types.InlineKeyboardButton("📊 عرض الإحصائيات", callback_data="stats"))
        markup.add(telebot.types.InlineKeyboardButton("🔄 تحديث الإحصائيات", callback_data="refresh_stats"))
        bot.send_message(message.chat.id, "📋 لوحة الأدمن:", reply_markup=markup)
    else:
        # لوحة المستخدم العادي
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton("🎶 حمل صوت", callback_data="audio"))
        markup.add(telebot.types.InlineKeyboardButton("🎬 حمل فيديو", callback_data="video"))
        markup.add(telebot.types.InlineKeyboardButton("ℹ️ معلومات", callback_data="info"))
        bot.send_message(message.chat.id, "👋 أهلاً بك! اختار العملية:", reply_markup=markup)

# التعامل مع ضغط الأزرار
@bot.callback_query_handler(func=lambda call: True)
def button_handler(call):
    global download_count, downloaded_links

    # أزرار الأدمن
    if call.from_user.id == ADMIN_ID:
        if call.data == "add_channel":
            bot.send_message(call.message.chat.id, "✏️ أرسل اسم القناة لإضافتها (مثال: @YourChannel)")
        elif call.data == "del_channel":
            bot.send_message(call.message.chat.id, "✏️ أرسل اسم القناة لحذفها")
        elif call.data == "list_channels":
            bot.send_message(call.message.chat.id, "📋 القنوات المطلوبة: (ميزة شكلية فقط حالياً)")
        elif call.data in ["stats", "refresh_stats"]:
            top_links = Counter(downloaded_links).most_common(5)
            table_header = "| الترتيب | الرابط | مرات التحميل |\n|---------|--------|---------------|\n"
            table_rows = ""
            if top_links:
                for i, (link, count) in enumerate(top_links, start=1):
                    table_rows += f"| {i} | {link} | {count} |\n"
            else:
                table_rows = "| - | لا توجد روابط | - |\n"

            stats_text = (
                f"📊 **الإحصائيات**\n\n"
                f"👥 عدد المستخدمين: {len(users)}\n"
                f"📥 عدد التحميلات: {download_count}\n\n"
                f"🔥 **أكثر 5 روابط:**\n\n"
                f"{table_header}{table_rows}"
            )
            bot.send_message(call.message.chat.id, stats_text, parse_mode="Markdown")

    # أزرار المستخدم العادي
    else:
        if call.data == "audio":
            bot.send_message(call.message.chat.id, "⏳ جاري التحميل كصوت...")
            try:
                file_path = download_youtube("https://www.youtube.com/watch?v=xSKtOXLoRhA", "audio.mp3")
                bot.send_audio(call.message.chat.id, open(file_path, "rb"))
                download_count += 1
                downloaded_links.append("https://www.youtube.com/watch?v=xSKtOXLoRhA")
            except Exception as e:
                bot.send_message(call.message.chat.id, f"❌ خطأ في التحميل: {e}")
        elif call.data == "video":
            bot.send_message(call.message.chat.id, "⏳ جاري التحميل كفيديو...")
            try:
                file_path = download_youtube("https://www.youtube.com/watch?v=xSKtOXLoRhA", "video.mp4")
                bot.send_video(call.message.chat.id, open(file_path, "rb"))
                download_count += 1
                downloaded_links.append("https://www.youtube.com/watch?v=xSKtOXLoRhA")
            except Exception as e:
                bot.send_message(call.message.chat.id, f"❌ خطأ في التحميل: {e}")
        elif call.data == "info":
            bot.send_message(call.message.chat.id, "ℹ️ معلومات الفيديو: العنوان - المدة - الحجم")

bot.infinity_polling()
