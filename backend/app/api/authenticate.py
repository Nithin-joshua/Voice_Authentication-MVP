from fastapi import APIRouter, UploadFile, File, Form
import shutil
import os
import time
import numpy as np

from app.core.feature_extractor import extract_mfcc
from app.core.matcher import (
    cosine_similarity,
    variance_distance,
    temporal_consistency
)
from app.utils.audio_utils import validate_audio
from app.db.postgres import load_voice_by_email
from app.db.redis import get_cached_features, get_redis

router = APIRouter()

UPLOAD_DIR = "audio/temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Thresholds
BASE_SIMILARITY_THRESHOLD = 0.80
VARIANCE_THRESHOLD = 2.5
TEMPORAL_THRESHOLD = 15.0

# Score fusion
FINAL_SCORE_THRESHOLD = 0.75

# Rate limiting
MAX_ATTEMPTS = 5
ATTEMPT_WINDOW = 600  # seconds

# Challenge
CHALLENGE_TTL_SECONDS = 60


@router.post("/authenticate")
async def authenticate_voice(
    email: str = Form(...),
    file: UploadFile = File(...)
):
    r = get_redis()
    if not r:
        return {"authenticated": False, "reason": "Security services unavailable"}

    # --------------------------------------------------
    # 1️⃣ RATE LIMIT CHECK
    # --------------------------------------------------
    attempt_key = f"auth_attempts:{email}"
    attempts = int(r.get(attempt_key) or 0)

    if attempts >= MAX_ATTEMPTS:
        return {
            "authenticated": False,
            "reason": "Too many failed attempts. Try later."
        }

    # --------------------------------------------------
    # 2️⃣ CHALLENGE–RESPONSE (LIVENESS)
    # --------------------------------------------------
    challenge_key = f"challenge:{email}"
    challenge_data = r.hgetall(challenge_key)

    if not challenge_data:
        return {"authenticated": False, "reason": "Challenge expired or missing"}

    issued_at = int(challenge_data.get(b"issued_at", b"0"))
    if time.time() - issued_at > CHALLENGE_TTL_SECONDS:
        r.delete(challenge_key)
        return {"authenticated": False, "reason": "Challenge expired"}

    # One-time use (anti-replay)
    r.delete(challenge_key)

    # --------------------------------------------------
    # 3️⃣ SAVE AUDIO
    # --------------------------------------------------
    audio_path = os.path.join(UPLOAD_DIR, "login.wav")
    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # --------------------------------------------------
    # 4️⃣ AUDIO QUALITY VALIDATION (NEW)
    # --------------------------------------------------
    is_valid, reason = validate_audio(audio_path)
    if not is_valid:
        return {"authenticated": False, "reason": reason}

    # --------------------------------------------------
    # 5️⃣ LOAD USER PROFILE
    # --------------------------------------------------
    user_id, mean_vector, std_vector = load_voice_by_email(email)

    if mean_vector is None:
        return {"authenticated": False, "reason": "User not found"}

    cached = get_cached_features(user_id)
    if cached is not None:
        mean_vector = cached

    # --------------------------------------------------
    # 6️⃣ FEATURE EXTRACTION
    # --------------------------------------------------
    test_vector = extract_mfcc(audio_path)
    segments = np.array_split(test_vector, 3)

    # --------------------------------------------------
    # 7️⃣ METRIC COMPUTATION + SCORE FUSION
    # --------------------------------------------------
    similarity = cosine_similarity(mean_vector, test_vector)
    variance_score = variance_distance(test_vector, mean_vector, std_vector)
    temporal_score = temporal_consistency(segments)

    variance_penalty = max(0.0, 1 - (variance_score / VARIANCE_THRESHOLD))
    temporal_norm = min(1.0, temporal_score / TEMPORAL_THRESHOLD)

    final_score = (
        0.5 * similarity +
        0.3 * variance_penalty +
        0.2 * temporal_norm
    )

    authenticated = final_score >= FINAL_SCORE_THRESHOLD

    # --------------------------------------------------
    # 8️⃣ RATE LIMIT UPDATE
    # --------------------------------------------------
    if authenticated:
        r.delete(attempt_key)
    else:
        r.incr(attempt_key)
        r.expire(attempt_key, ATTEMPT_WINDOW)

    return {
        "email": email,
        "similarity_score": round(similarity, 3),
        "variance_score": round(variance_score, 3),
        "temporal_score": round(temporal_score, 3),
        "final_score": round(final_score, 3),
        "authenticated": authenticated
    }
