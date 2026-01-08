from fastapi import APIRouter, UploadFile, File, Form
import shutil
import os
import numpy as np

from app.core.feature_extractor import extract_mfcc
from app.core.audio_utils import validate_audio
from app.db.postgres import save_user
from app.db.redis import cache_features

router = APIRouter()

UPLOAD_DIR = "audio/temp"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/enroll")
async def enroll_voice(
    name: str = Form(...),
    email: str = Form(...),
    file1: UploadFile = File(...),
    file2: UploadFile = File(...),
    file3: UploadFile = File(...)
):
    audio_files = [file1, file2, file3]
    feature_vectors = []

    for idx, file in enumerate(audio_files):
        audio_path = os.path.join(UPLOAD_DIR, f"enroll_{idx}.wav")

        # Save audio
        with open(audio_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # -----------------------------
        # 🔐 AUDIO QUALITY VALIDATION
        # -----------------------------
        is_valid, reason = validate_audio(audio_path)
        if not is_valid:
            return {
                "error": f"Enrollment failed (sample {idx + 1}): {reason}"
            }

        # Feature extraction
        mfcc = extract_mfcc(audio_path)
        feature_vectors.append(mfcc)

    # -----------------------------
    # 📊 MULTI-SAMPLE PROFILING
    # -----------------------------
    features_stack = np.vstack(feature_vectors)
    mean_vector = np.mean(features_stack, axis=0)
    std_vector = np.std(features_stack, axis=0)

    # Save user profile
    user_id = save_user(name, email, mean_vector, std_vector)

    # Cache mean vector for fast auth
    cache_features(user_id, mean_vector)

    return {
        "message": "Enrollment successful with multi-sample voice profiling",
        "email": email
    }
