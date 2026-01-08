from fastapi import APIRouter, Depends
from app.dependencies.admin_auth import require_admin
from app.db.postgres import get_auth_logs

router = APIRouter(
    prefix="/admin/logs",
    tags=["Admin Logs"]
)

@router.get("/")
def view_logs(
    admin_email: str = Depends(require_admin),
    limit: int = 100
):
    logs = get_auth_logs(limit)
    return {
        "admin": admin_email,
        "count": len(logs),
        "logs": logs
    }
