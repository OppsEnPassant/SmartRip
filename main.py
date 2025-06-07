from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from media_downloader import download_video_with_audio, transcribe_audio

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/process", response_class=JSONResponse)
async def process(
    request: Request,
    url: str = Form(...),
    quality: str = Form("best"),
    is_playlist: str = Form("n"),
    filename_template: str = Form("%(title)s"),
    transcribe: str = Form("n")
):
    try:
        download_all = is_playlist.lower() == "y"
        do_transcribe = transcribe.lower() == "y"

        info = download_video_with_audio(
            url, quality=quality, download_all=download_all, filename_template=filename_template
        )

        transcription = None
        if do_transcribe and "filepath" in info:
            transcription = transcribe_audio(info["filepath"])

        return {
            "success": True,
            "info": info,
            "transcription": transcription,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
