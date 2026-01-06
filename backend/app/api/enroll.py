from fastapi import APIRouter, UploadFile, File
import shutil
import os
import numpy as np

from app.core.feature_extractor import extract_mfcc

router = APIRouter()

UPLOAD_DIR = "audio/temp"
FEATURE_PATH = "audio/enrolled_voice.npy"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/enroll")
async def enroll_voice(file: UploadFile = File(...)):
    audio_path = os.path.join(UPLOAD_DIR, "enroll.wav")

    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    features = extract_mfcc(audio_path)
    np.save(FEATURE_PATH, features)

    return {
        "message": "Voice enrolled successfully",
        "feature_length": len(features)
    }
