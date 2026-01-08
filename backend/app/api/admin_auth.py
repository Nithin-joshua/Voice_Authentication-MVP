from fastapi import APIRouter, HTTPException
from app.models.admin import AdminLogin
from app.utils.security import verify_password
from app.db.admin import get_admin_by_email
from app.utils.jwt import create_access_token

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/login")
def admin_login(data: AdminLogin):
    admin = get_admin_by_email(data.email)
    if not admin or not verify_password(data.password, admin["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": data.email})
    return {"access_token": token}
