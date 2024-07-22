
import os
from typing import Annotated
from urllib import request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, File, HTTPException, Request, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import datetime

app = FastAPI()

origins = ["*"]
content_path = "content/"

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def index():
    return FileResponse('static/index.html')

@app.post("/api/upload")
async def upload(file: UploadFile, dir: Annotated[str, Form()]):
    if str(dir).count(".") > 0 or str(dir).count(":") > 0:
        raise HTTPException(status_code=400,
                            detail="dir contains forbidden symbols")
    if not os.path.exists(content_path + dir):
        os.makedirs(content_path + dir)
    print("start upload \t\t" + file.filename + "\t\t" + str(datetime.datetime.now().time()))
    new_file = open(content_path + dir + "/" + file.filename, "wb+")
    new_file.write(file.file.read())
    return {"succes"}