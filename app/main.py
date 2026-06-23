from contextlib import asynccontextmanager
from fastapi import FastAPI

from services.oauth_service import OauthService
from services.clients_service import ClientService
from api import api_routes
from jat import TokenManager


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.token_manager = TokenManager()
    app.state.oauth_service = OauthService()
    app.state.clients_service = ClientService()

    yield

app = FastAPI(lifespan=lifespan)


app.include_router(api_routes())
