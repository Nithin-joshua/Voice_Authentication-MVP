from fastapi import APIRouter, UploadFile, File, Form
import shutil
import os
import time

from app.core.feature_extractor import extract_mfcc
from app.core.matcher import cosine_similarity, variance_distance
from app.db.postgres import load_voice_by_email
from app.db.redis import get_cached_features, get_redis

router = APIRouter()

UPLOAD_DIR = "audio/temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

BASE_SIMILARITY_THRESHOLD = 0.80
VARIANCE_THRESHOLD = 2.5
CHALLENGE_TTL_SECONDS = 60


@router.post("/authenticate")
async def authenticate_voice(
    email: str = Form(...),
    file: UploadFile = File(...)
):
    # -----------------------------
    # 1️⃣ LIVENESS CHECK (CHALLENGE)
    # -----------------------------
    r = get_redis()
    if not r:
        return {"authenticated": False, "reason": "Liveness service unavailable"}

    challenge_key = f"challenge:{email}"
    challenge_data = r.hgetall(challenge_key)

    if not challenge_data:
        return {"authenticated": False, "reason": "Challenge expired or missing"}

    issued_at = int(challenge_data.get(b"issued_at", b"0"))
    if time.time() - issued_at > CHALLENGE_TTL_SECONDS:
        r.delete(challenge_key)
        return {"authenticated": False, "reason": "Challenge expired"}

    # One-time use → prevents replay
    r.delete(challenge_key)

 
    # 2️⃣ SAVE AUDIO
    audio_path = os.path.join(UPLOAD_DIR, "login.wav")
    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # -----------------------------
    # 3️⃣ LOAD USER VOICE PROFILE
    # -----------------------------
    user_id, mean_vector, std_vector = load_voice_by_email(email)

    if mean_vector is None:
        return {"authenticated": False, "reason": "User not found"}

    cached = get_cached_features(user_id)
    if cached is not None:
        mean_vector = cached

    # -----------------------------
    # 4️⃣ FEATURE EXTRACTION
    # -----------------------------
    test_vector = extract_mfcc(audio_path)

    # -----------------------------
    # 5️⃣ STATISTICAL AUTHENTICATION
    # -----------------------------
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
