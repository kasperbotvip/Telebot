import yt_dlp
import os

def download_media(url, mode="video"):
    # إعدادات مشتركة
    ydl_opts = {
        "noplaylist": True,
        "concurrent_fragment_downloads": 1,
        "geo_bypass": True,
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        },
        "extractor_args": {
            "youtube": {
                "player_client": ["web"],
            }
        }
    }

    # إعدادات حسب النوع
    if mode == "audio":
        ydl_opts.update({
            "format": "bestaudio/best",
            "outtmpl": "audio.%(ext)s",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "m4a",  # تقدر تخليها "mp3" إذا تحب
                    "preferredquality": "192",
                }
            ],
        })
    else:
        ydl_opts.update({
            "format": "bestvideo+bestaudio/best",
            "merge_output_format": "mp4",
            "outtmpl": "video.%(ext)s",
        })

    # استخدام ملف الكوكيز (الخيار الصحيح: cookiefile)
    if os.path.exists("cookies.txt"):
        ydl_opts["cookiefile"] = "cookies.txt"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filepath = ydl.prepare_filename(info)

        # تصحيح اسم ملف الصوت بعد التحويل (yt-dlp قد يغير الامتداد)
        if mode == "audio":
            base = os.path.splitext(filepath)[0]
            m4a_path = base + ".m4a"
            mp3_path = base + ".mp3"
            if os.path.exists(m4a_path):
                return m4a_path
            if os.path.exists(mp3_path):
                return mp3_path

        return filepath
