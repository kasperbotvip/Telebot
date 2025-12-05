import yt_dlp
import os

def download_social(url, mode="video"):
    ydl_opts = {
        "noplaylist": True,
        "concurrent_fragment_downloads": 1,
        "geo_bypass": True,
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
