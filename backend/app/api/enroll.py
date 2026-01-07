from fastapi import APIRouter, UploadFile, File, Form
import shutil
import os

from app.core.feature_extractor import extract_mfcc
from app.db.postgres import save_user
from app.db.redis import cache_features

router = APIRouter()

UPLOAD_DIR = "audio/temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/enroll")
async def enroll_voice(
    name: str = Form(...),
    email: str = Form(...),
    file: UploadFile = File(...)
):
    audio_path = os.path.join(UPLOAD_DIR, "enroll.wav")

    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    features = extract_mfcc(audio_path)

    user_id = save_user(name, email, features)
    cache_features(user_id, features)

    return {
        "message": "Enrollment successful",
        "email": email
    }
