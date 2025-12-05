import yt_dlp
import os

def download_media(url, mode="video"):
    ydl_opts = {
        # تيمبلت الإخراج
        "outtmpl": "audio.%(ext)s" if mode == "audio" else "video.%(ext)s",
        # اختيار الجودة/الصيغة
        "format": "bestaudio/best" if mode == "audio" else "bestvideo+bestaudio/best",
        "merge_output_format": "mp4" if mode == "video" else None,

        # إعدادات تقلل المشاكل
        "noplaylist": True,
        "concurrent_fragment_downloads": 1,
        "geo_bypass": True,

        # هيدر واضح حتى ما يعتبرك بوت بسهولة
        "http_headers": {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        },

        # تلميحات للمستخرج الخاص بيوتيوب
        "extractor_args": {
            "youtube": {
                "player_client": ["web"],  # استخدم عميل 'web' بدل 'android/ios'
                "skip": ["dash"]           # يقلل اعتماد مشغّل DASH إذا سبب مشكلة
            }
        }
    }

    # ✅ الخيار الصحيح في بايثون: cookiefile
    if os.path.exists("cookies.txt"):
        ydl_opts["cookiefile"] = "cookies.txt"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)
