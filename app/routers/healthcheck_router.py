from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/liveness")
def liveness():
    """Проверка, работает ли приложение"""

    return {"message": "OK"}