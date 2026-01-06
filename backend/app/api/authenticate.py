from fastapi import APIRouter, UploadFile, File
import shutil
import os
import numpy as np

from app.core.feature_extractor import extract_mfcc
from app.core.matcher import cosine_similarity
from app.core.threshold import is_authenticated

router = APIRouter()

UPLOAD_DIR = "audio/temp"
FEATURE_PATH = "audio/enrolled_voice.npy"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/authenticate")
async def authenticate_voice(file: UploadFile = File(...)):
    if not os.path.exists(FEATURE_PATH):
        return {"error": "No enrolled voice found"}

    audio_path = os.path.join(UPLOAD_DIR, "login.wav")

    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    enrolled = np.load(FEATURE_PATH)
    test = extract_mfcc(audio_path)

    score = cosine_similarity(enrolled, test)

    return {
        "similarity_score": round(score, 3),
        "authenticated": is_authenticated(score)
    }
