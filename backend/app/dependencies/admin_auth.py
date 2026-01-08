from fastapi import Depends, HTTPException, Header
from app.utils.jwt import decode_access_token

def require_admin(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")

    token = authorization.split(" ")[1]
    payload = decode_access_token(token)

    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload["sub"]  # admin email
