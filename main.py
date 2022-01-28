import os
from pathlib import Path
from unicodedata import name
from fastapi import FastAPI, Request, status
from pytube import YouTube
from fastapi.templating import Jinja2Templates
from fastapi import BackgroundTasks
from fastapi.responses import FileResponse, RedirectResponse
import tempfile
import uuid

# https://www.studytonight.com/post/pytube-to-download-youtube-videos-with-python

app = FastAPI()
templates = Jinja2Templates(directory="templates")
temdir = Path.cwd() / "tmp"


def get_all_video_mp4(link_video: str):
    pass

    # TODO: Hacer una seccion solo para videos MP4
    """
        TODO: Listar las calidades disponibles del video
        TODO: Seleccionar todos los videos en mp4
        TODO: Filtrar los videos que tenga un type Nope
        TODO: Seleccionar un video especifico
        TODO: descargar el video en el ordenador
    """


# TODO: Hacer una seccion solo para audio
def download_video(link_video, itag):
    global tempdir
    dir = str(temdir)
    yt = YouTube(link_video)
    download_path = yt.streams.get_by_itag(int(itag))
    print(f"[INFO] -> {download_path}")
    tempname = str(uuid.uuid4()) + ".mp4"
    name = yt.title + ".mp4"
    path = download_path.download(output_path=dir, filename=tempname)
    return name, tempname


def delete_file(filename):
    global temdir
    print("File is delete")
    os.unlink(str(temdir/ filename))


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/video")
async def video(request: Request):
    form_data = await request.form()
    link_video = form_data.get("url_video", None)
    itag = form_data.get("optionDownload", None)
    print(f"[FORM]: -> {form_data}")
    (name, tempname) = download_video(link_video, itag)
    print(form_data.get("url_video"))

    return {"name": name, "tempname": tempname}


@app.get("/video")
async def download(
    tempname: str, name_video: str, request: Request, backgroundTasks: BackgroundTasks
):
    backgroundTasks.add_task(delete_file, tempname)
    return FileResponse(
        path=(temdir / tempname),
        media_type="files/mp4",
        filename=name_video,
    )


@app.post("/list_format")
async def list_format(request: Request):
    form_data = await request.form()
    print(form_data)
    link_video = form_data.get("url_video", None)

    if link_video is None:
        return {}
    resolution = {
        "720p": 0.0,
        "360p": 0.0,
        "144p": 0.0,
    }
    videos = resolution
    yt = YouTube(link_video)
    filter_video = yt.streams.filter(progressive=True)
    for i, video in enumerate(filter_video):
        try:
            if video.type == "video":
                current_size = round(video.filesize / 1024 / 1024, 2)
                previus_size = resolution.get(video.resolution, 0.0)
                if current_size > previus_size:
                    resolution[video.resolution] = current_size
                    videos[video.resolution] = {
                        "res": video.resolution,
                        "itag": video.itag,
                        "size": current_size,
                        "fps": video.fps,
                    }

        except Exception as ex:
            # print(f"[ERROR] -> {ex}")
            continue

    return videos
