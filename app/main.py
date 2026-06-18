from contextlib import asynccontextmanager
from fastapi import FastAPI

from routers import oauth
from services.oauth_service import OauthService


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.oauth_service = OauthService()

    yield

app = FastAPI(lifespan=lifespan)

app.include_router(oauth.router)

@app.get("/")
def root():
    return {"message": "Hello World"}