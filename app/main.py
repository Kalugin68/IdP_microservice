from contextlib import asynccontextmanager
from fastapi import FastAPI

from repositories.clients import ClientRepository
from repositories.oauth_codes import OAuthRepository
from repositories.users import UserRepository
from routers import oauth_router, healthcheck_router
from services.oauth_service import OauthService
from services.token_service import Token
from config.settings import Settings
from config.database import DBConfig


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()

    db_config = DBConfig(
        db_user=settings.db_user,
        db_password=settings.db_password,
        db_host=settings.db_host,
        db_port=settings.db_port,
        db_name=settings.db_name
    )
    app.state.db_config = db_config

    app.state.user_repo = UserRepository(db_config.engine)
    app.state.client_repo = ClientRepository(db_config.engine)
    app.state.oauth_repo = OAuthRepository(db_config.engine)

    app.state.token_service = Token(secret_key=settings.jwt_secret)
    app.state.oauth_service = OauthService()

    yield

app = FastAPI(lifespan=lifespan)

app.include_router(oauth_router.router)
app.include_router(healthcheck_router.router)

@app.get("/")
def root():
    return {"message": "Hello World"}