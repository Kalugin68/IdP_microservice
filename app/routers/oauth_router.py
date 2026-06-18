from fastapi import APIRouter, Request
from schemas.oauth import TokenRequest, AuthorizeRequest


router = APIRouter(prefix="/oauth", tags=["OAuth"])

@router.post("/authorize")
def authentication_route(request:Request, data: AuthorizeRequest):
    """Маршрут аутентификации пользователя"""

    return request.app.state.oauth_service.authentication(data.login, data.password)

@router.post("/token")
def token_route(request: Request, data: TokenRequest):
    """Маршрут получения токена для авторизации у клиента"""

    return request.app.state.oauth_service.authorization(
        data.authorization_code, data.client_id, data.client_secret, request)