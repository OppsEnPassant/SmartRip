import yt_dlp
import os

def download_video_with_audio(
    url,
    output_path="downloads",
    filename_template="%(title)s",
    download_all=True,
    quality="best"
):
    os.makedirs(output_path, exist_ok=True)

    output_template = os.path.join(output_path, f"{filename_template}.%(ext)s")

    # Determine the format string based on user preference
    format_string = {
        "best": "bestvideo+bestaudio/best",
        "worst": "worstvideo+worstaudio/worst",
        "audio": "bestaudio",
        "video": "bestvideo",
    }.get(quality.lower(), quality)  # allow custom strings like '720p'

    ydl_opts = {
        'format': format_string,
        'merge_output_format': 'mp4',
        'outtmpl': output_template,
        'noplaylist': not download_all,
        'postprocessors': [
            {
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }
        ],
        'quiet': False
    }

    print(f"\n🎯 Downloading using format: {format_string}")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    print("✅ Download complete.")
    return info
