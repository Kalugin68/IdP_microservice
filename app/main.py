from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from starlette.responses import JSONResponse

from exceptions import ServiceException
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


@app.exception_handler(ServiceException)
def service_exception_handler(request: Request, exc: ServiceException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.msg
        }
    )


@app.exception_handler(Exception)
def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal Server Error"
        }
    )