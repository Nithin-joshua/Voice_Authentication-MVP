from app.api import admin_logs
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File
import os
import shutil
from app.api import enroll, authenticate
from fastapi.middleware.cors import CORSMiddleware
from app.api import admin_auth
from app.api import admin_users

app = FastAPI(title="Voice Authentication Backend")
app.include_router(admin_auth.router)
app.include_router(admin_users.router)
app.include_router(admin_logs.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(enroll.router)
app.include_router(authenticate.router)

UPLOAD_DIR = "audio/temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/health")
def health_check():
    return {"status": "Backend is running"}


@app.post("/upload-test")
async def upload_audio(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "message": "Audio uploaded successfully"
    }
