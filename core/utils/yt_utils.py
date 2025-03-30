import re
import urllib.request
import yt_dlp
from core.ydl_opts import ydl_opts


def get_video_url(query) -> str:
    if "youtube.com" in query or "youtu.be" in query:
        return query
    search_keyword = query.replace(" ", "+")
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    return "https://www.youtube.com/watch?v=" + video_ids[0]


def get_audio_stream(url) -> dict:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info