from fastapi import APIRouter
import random
import string
import time
import os

from app.db.redis import get_redis

router = APIRouter()

CHALLENGE_TTL_SECONDS = 60

PHRASES = [
    "my voice confirms my identity",
    "authenticate access now",
    "secure voice login",
    "voice verification in progress",
]

def random_digits():
    return " ".join(str(random.randint(0, 9)) for _ in range(3))

@router.get("/challenge")
def get_challenge(email: str):
    r = get_redis()
    if not r:
        return {"error": "Redis not available"}

    # Mix phrase + digits to avoid replay
    phrase = random.choice(PHRASES)
    digits = random_digits()
    challenge = f"{phrase} {digits}"

    key = f"challenge:{email}"
    payload = {
        "text": challenge,
        "issued_at": int(time.time())
    }

    r.hset(key, mapping=payload)
    r.expire(key, CHALLENGE_TTL_SECONDS)

    return {
        "challenge": challenge,
        "expires_in": CHALLENGE_TTL_SECONDS
    }
