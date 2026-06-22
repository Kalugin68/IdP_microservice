from fastapi import APIRouter, Request
from schemas.oauth import TokenRequest, AuthorizeRequest


router = APIRouter(prefix="/oauth", tags=["OAuth"])

@router.post("/authorize")
async def authentication_route(request:Request, data: AuthorizeRequest):
    """Маршрут аутентификации пользователя"""

    return await request.app.state.oauth_service.authentication(request, data.login, data.password)

@router.post("/token")
async def token_route(request: Request, data: TokenRequest):
    """Маршрут получения токена для авторизации у клиента"""

    return await request.app.state.oauth_service.authorization(request,
        data.authorization_code, data.client_id, data.client_secret)