ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors':
        {
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'opus',
        },
    'extractaudio': True,
    'audioformat': 'opus',
    'noplaylist': True,
    'quiet': True,
    'no_warnings': True,
}