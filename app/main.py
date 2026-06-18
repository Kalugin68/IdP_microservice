from contextlib import asynccontextmanager
from fastapi import FastAPI

from routers import oauth_router, healthcheck_router
from services.oauth_service import OauthService
from services.token_service import Token
from config.settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()

    app.state.token_service = Token(secret_key=settings.jwt_secret)
    app.state.oauth_service = OauthService()

    yield

app = FastAPI(lifespan=lifespan)

app.include_router(oauth_router.router)
app.include_router(healthcheck_router.router)

@app.get("/")
def root():
    return {"message": "Hello World"}