from fastapi import APIRouter, Depends
from app.dependencies.admin_auth import require_admin

router = APIRouter(
    prefix="/admin/users",
    tags=["Admin Users"]
)

@router.get("/")
def list_users(admin_email: str = Depends(require_admin)):
    return {
        "message": "Admin access granted",
        "admin": admin_email
    }
