import yt_dlp
import os
import whisper

# Function to download a single video or audio
def download_video_with_audio(url, quality="best", filename_template="%(title)s.%(ext)s", download_all=False):
    ydl_opts = {
        "format": quality,
        "outtmpl": filename_template,
        "merge_output_format": "mp4",  # Ensure audio + video are merged
        "postprocessors": [{
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4"
        }]
    }

    downloaded_files = []

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=not download_all)
        
        if "_type" in info and info["_type"] == "playlist" and download_all:
            for entry in info["entries"]:
                video_url = entry["webpage_url"]
                ydl.download([video_url])
                filename = ydl.prepare_filename(entry).rsplit('.', 1)[0] + ".mp4"
                downloaded_files.append(filename)
        else:
            filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + ".mp4"
            downloaded_files.append(filename)

    return downloaded_files

# Function to transcribe audio from a downloaded file
def transcribe_audio(audio_path, language="en"):
    model = whisper.load_model("base")
    print(f"Transcribing {audio_path}...")
    result = model.transcribe(audio_path, language=language)
    text = result["text"]

    # Save transcript
    txt_path = os.path.splitext(audio_path)[0] + ".txt"
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text)

    return text
o
