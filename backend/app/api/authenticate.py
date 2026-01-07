from fastapi import APIRouter, UploadFile, File, Form
import shutil
import os

from app.core.feature_extractor import extract_mfcc
from app.core.matcher import cosine_similarity, variance_distance
from app.db.postgres import load_voice_by_email
from app.db.redis import get_cached_features

router = APIRouter()

UPLOAD_DIR = "audio/temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

BASE_SIMILARITY_THRESHOLD = 0.80
VARIANCE_THRESHOLD = 2.5

@router.post("/authenticate")
async def authenticate_voice(
    email: str = Form(...),
    file: UploadFile = File(...)
):
    audio_path = os.path.join(UPLOAD_DIR, "login.wav")

    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    user_id, mean_vector, std_vector = load_voice_by_email(email)

    if mean_vector is None:
        return {"authenticated": False, "reason": "User not found"}

    cached = get_cached_features(user_id)
    if cached is not None:
        mean_vector = cached

    test_vector = extract_mfcc(audio_path)

    similarity = cosine_similarity(mean_vector, test_vector)
    variance_score = variance_distance(test_vector, mean_vector, std_vector)

    authenticated = (
        similarity >= BASE_SIMILARITY_THRESHOLD
        and variance_score <= VARIANCE_THRESHOLD
    )

    return {
        "email": email,
        "similarity_score": round(similarity, 3),
        "variance_score": round(variance_score, 3),
        "authenticated": authenticated
    }
