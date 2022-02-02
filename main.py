import os
from pathlib import Path
from unicodedata import name
from fastapi import FastAPI, Request, status
from pytube import YouTube
from fastapi.templating import Jinja2Templates
from fastapi import BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import tempfile
import uuid

# https://www.studytonight.com/post/pytube-to-download-youtube-videos-with-python
# https://github.com/pytube/pytube/issues/1218

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")
temdir = Path.cwd() / "tmp"

def download_video(link_video, itag):
    """[summary]

    Args:
        link_video ([str]): [url of video]
        itag ([int]): [itag is id of video select]

    Returns:
        [(name,tempname)]: [return name of video and temporal name]
    """
    global tempdir
    dir = str(temdir)
    yt = YouTube(link_video)
    download_path = yt.streams.get_by_itag(int(itag))
    print(f"[INFO] -> {download_path}")
    tempname = str(uuid.uuid4()) + ".mp4"
    name = yt.title + ".mp4"
    path = download_path.download(output_path=dir, filename=tempname)
    return (name, tempname)


def delete_file(filename):
    """[Delete file with temporal name]

    Args:
        filename ([str]): [temporal name of video]
    """
    global temdir
    os.unlink(str(temdir / filename))
    print("File is delete")


@app.get("/")
async def home(request: Request):
    """[Route main to show template to download video]

    Args:
        request (Request): [description]

    Returns:
        [type]: [description]
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/video")
async def video(request: Request):
    """[summary]

    Args:
        request (Request): [description]

    Returns:
        [type]: [description]
    """
    form_data = await request.form()
    link_video = form_data.get("url_video", None)
    itag = form_data.get("optionDownload", None)
    (name, tempname) = download_video(link_video, itag)
    print(form_data.get("url_video"))

    return {"name": name, "tempname": tempname}


@app.get("/video")
async def download(
    tempname: str, name_video: str, request: Request, backgroundTasks: BackgroundTasks
):
    """[summary]

    Args:
        tempname (str): [temporal name]
        name_video (str): [name of video]
        request (Request): [description]
        backgroundTasks (BackgroundTasks): [class to exec proccess in background to delete file]

    Returns:
        [type]: [description]
    """
    backgroundTasks.add_task(delete_file, tempname)
    return FileResponse(
        path=(temdir / tempname),
        media_type="files/mp4",
        filename=name_video,
    )


@app.post("/list_format")
async def list_format(request: Request):
    """[Select the video qualities which work for downloading and return a json of the options. ]

    Args:
        request (Request): [form input send client]

    Returns:
        [dict]: [dict of video qualities]
    """
    form_data = await request.form()
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
            continue

    return videos
