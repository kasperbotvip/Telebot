def post_to_social(media_path, platform):
    platforms = {
        "instagram": "📸 إنستغرام",
        "facebook": "📘 فيسبوك",
        "twitter": "🐦 تويتر/X",
        "tiktok": "🎵 تيك توك",
        "youtube": "▶️ يوتيوب",
        "telegram": "✈️ تلجرام"
    }
    if platform in platforms:
        return f"✅ تم تجهيز {media_path} للنشر على {platforms[platform]}"
    else:
        return f"⚠️ المنصة {platform} غير مدعومة حالياً"
