import os
import re
import yt_dlp
from pathlib import Path
from typing import Optional
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# ضع توكن البوت هنا
BOT_TOKEN = "6188422479:AAEjeLAGKvXnPyrmA94VcPpuedvboKtZ5fE"

DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)

MAX_VIDEO_SIZE = 45 * 1024 * 1024
MAX_AUDIO_SIZE = 20 * 1024 * 1024
URL_RE = re.compile(r"https?://[^\s]+")

def download_media(url: str, audio_only: bool = False) -> Optional[Path]:
    ydl_opts = {
        "outtmpl": str(DOWNLOAD_DIR / "%(title)s.%(ext)s"),
        "quiet": True,
        "noplaylist": True,
        "format": "bestaudio/best" if audio_only else "bv*+ba/b",
    }
    if audio_only:
        ydl_opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return Path(ydl.prepare_filename(info))
    except Exception:
        return None

async def send_file(update: Update, file_path: Path, audio_only: bool):
    size = file_path.stat().st_size
    caption = f"✅ تم التحميل: {file_path.name}"
    try:
        if audio_only:
            if size > MAX_AUDIO_SIZE:
                await update.message.reply_document(document=open(file_path, "rb"), caption=caption)
            else:
                await update.message.reply_audio(audio=open(file_path, "rb"), caption=caption)
        else:
            if size > MAX_VIDEO_SIZE:
                await update.message.reply_document(document=open(file_path, "rb"), caption=caption)
            else:
                await update.message.reply_video(video=open(file_path, "rb"), caption=caption)
    finally:
        file_path.unlink(missing_ok=True)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if not URL_RE.match(text):
        await update.message.reply_text("📌 أرسل رابط فيديو مباشر ليتم تحميله.")
        return

    await update.message.reply_text("⏳ جاري التحميل...")

    audio_only = "audio" in text.lower()
    file_path = download_media(text, audio_only=audio_only)
    if not file_path:
        await update.message.reply_text("❌ تعذر التحميل. تحقق من الرابط أو جرب لاحقاً.")
        return

    await send_file(update, file_path, audio_only=audio_only)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🚀 البوت شغال... أرسل رابط فيديو")
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
