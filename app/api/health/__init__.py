from fastapi import APIRouter


router = APIRouter(prefix="/health", tags=["health"])


@router.get("/liveness")
def liveness():
    return {"message": "OK"}