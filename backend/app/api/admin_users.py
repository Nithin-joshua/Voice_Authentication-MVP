from fastapi import APIRouter, Depends, HTTPException
from app.dependencies.admin_auth import require_admin
from app.db.admin import get_all_users, set_user_status

router = APIRouter(
    prefix="/admin/users",
    tags=["Admin Users"]
)

@router.get("/")
def list_users(admin_email: str = Depends(require_admin)):
    users = get_all_users()
    return {
        "admin": admin_email,
        "total_users": len(users),
        "users": users
    }

@router.post("/{user_id}/disable")
def disable_user(
    user_id: str,
    admin_email: str = Depends(require_admin)
):
    set_user_status(user_id, False)
    return {
        "message": "User disabled successfully",
        "user_id": user_id
    }

@router.post("/{user_id}/enable")
def enable_user(
    user_id: str,
    admin_email: str = Depends(require_admin)
):
    set_user_status(user_id, True)
    return {
        "message": "User enabled successfully",
        "user_id": user_id
    }
