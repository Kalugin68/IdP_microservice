from fastapi import APIRouter

from .health import router as HealthAPI
from .oauth import router as OAuthAPI
from .client import router as ClientAPI


def api_routes():
    router = APIRouter(prefix="/api")

    router.include_router(HealthAPI)
    router.include_router(OAuthAPI)
    router.include_router(ClientAPI)

    return router