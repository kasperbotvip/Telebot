import yt_dlp
import os

def download_media(url, mode="video"):
    ydl_opts = {
        "outtmpl": "audio.%(ext)s" if mode == "audio" else "video.%(ext)s",
        "format": "bestaudio/best" if mode == "audio" else "bestvideo+bestaudio/best",
        "merge_output_format": "mp4" if mode == "video" else None,
    }

    if os.path.exists("cookies.txt"):
        ydl_opts["cookies"] = "cookies.txt"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)
