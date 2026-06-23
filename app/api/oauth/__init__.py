from fastapi import APIRouter, Request

from .dto import TokenRequest, AuthorizeRequest


router = APIRouter(prefix="/oauth", tags=["OAuth"])


@router.post("/authorize")
async def authentication_route(request:Request, data: AuthorizeRequest):
    return await request.app.state.oauth_service.authentication(data.login, data.password)


@router.post("/token")
async def token_route(request: Request, data: TokenRequest):
    return await request.app.state.oauth_service.authorization(request,
        data.authorization_code, data.client_id, data.client_secret)