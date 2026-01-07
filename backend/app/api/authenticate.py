from fastapi import APIRouter, UploadFile, File, Form
import shutil
import os

from app.core.feature_extractor import extract_mfcc
from app.core.matcher import cosine_similarity
from app.core.threshold import is_authenticated
from app.db.postgres import load_voice_by_email
from app.db.redis import get_cached_features

router = APIRouter()

UPLOAD_DIR = "audio/temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/authenticate")
async def authenticate_voice(
    email: str = Form(...),
    file: UploadFile = File(...)
):
    audio_path = os.path.join(UPLOAD_DIR, "login.wav")

    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    user_id, enrolled_features = load_voice_by_email(email)

    if not enrolled_features.any():
        return {"error": "User not found"}

    # Redis cache check (optional)
    cached = get_cached_features(user_id)
    if cached is not None:
        enrolled_features = cached

    test_features = extract_mfcc(audio_path)
    score = cosine_similarity(enrolled_features, test_features)

    return {
        "email": email,
        "similarity_score": round(score, 3),
        "authenticated": is_authenticated(score)
    }
