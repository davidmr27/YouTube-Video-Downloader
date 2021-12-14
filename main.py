from fastapi import FastAPI
from pytube import YouTube

app = FastAPI()

def get_all_video_mp4(link_video:str):
    pass

#TODO: Hacer una seccion solo para videos MP4
#TODO: Hacer una seccion solo para audio

@app.get("/video")
async def video():
    yt = YouTube('https://www.youtube.com/watch?v=LXb3EKWsInQ')
    print(yt.title)
    print(yt.streams.filter(file_extension='mp4'))
    for i in yt.streams.filter(file_extension='mp4'):
        print(i)
    return {"message": "Hello world"}
