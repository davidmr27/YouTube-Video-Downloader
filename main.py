import os

import requests
from fastapi import FastAPI, Request, Form
from pytube import YouTube
from fastapi.templating import Jinja2Templates
from fastapi.responses import StreamingResponse, FileResponse
from fastapi import BackgroundTasks
import tempfile

# https://www.studytonight.com/post/pytube-to-download-youtube-videos-with-python

app = FastAPI()
templates = Jinja2Templates(directory="templates")


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
def download_video(link_video):
    yt = YouTube(link_video)
    result = yt.streams.filter(file_extension='mp4')
    download_path = result.get_highest_resolution()
    print(f"[INFO] -> {result}")
    extestions = download_path.mime_type.split('/')[-1]
    temppath = tempfile.NamedTemporaryFile(suffix='_temp.mp4', prefix='askvideo_')
    print(download_path)
    print(extestions)
    _, output_path, name = temppath.name.split('/')
    path = download_path.download(output_path=output_path, filename=name)
    return path, name, temppath


def delete_file(filename, path):
    filename.close()
    print('File is delete')
    os.remove(path)


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/")
async def video(request: Request, backgroundTasks: BackgroundTasks):
    form_data = await request.form()
    link_video = form_data.get('url_video', None)
    (path, name, temppath) = download_video(link_video)
    print(form_data.get('url_video'))
    backgroundTasks.add_task(delete_file, temppath, path)
    return FileResponse(path=temppath.name, media_type="video/mp4",
                        filename=name)
