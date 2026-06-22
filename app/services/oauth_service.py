from fastapi import HTTPException
from uuid import uuid4
from datetime import datetime, timedelta


class OauthService:
    """Класс для работы с авторизацией и аутентификацией"""

    async def authentication(self, request, login: str, password: str):
        """Возвращает код авторизации"""

        user = await request.app.state.user_repo.get_by_login(login)

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Неверные учетные данные",
            )

        if user["password"] != password:
            raise HTTPException(
                status_code=401,
                detail="Неверные учетные данные",
            )

        code = str(uuid4())
        expires_at = datetime.utcnow() + timedelta(minutes=5)

        await request.app.state.oauth_repo.create_code(code, login, expires_at)

        return {"authorization_code": code}

    async def authorization(self, request, code: str, client_id: str,
                      client_secret: str):
        """Возвращает JWT-токен"""

        client = await request.app.state.client_repo.get_by_client_id(client_id)

        if not client:
            raise HTTPException(
                status_code=401,
                detail="Неверные данные"
            )

        if client["client_secret"] != client_secret:
            raise HTTPException(
                status_code=401,
                detail="Неверные данные"
            )

        auth_code = await request.app.state.oauth_repo.get_code(code)

        if not auth_code:
            raise HTTPException(
                status_code=401,
                detail="Неверные данные"
            )

        if auth_code["expires_at"] < datetime.utcnow():
            await request.app.state.oauth_repo.delete_code(code)

            raise HTTPException(
                status_code=401,
                detail="Срок действия кода истек"
            )

        user = await request.app.state.user_repo.get_by_login(auth_code["login"])

        access_token = request.app.state.token_service.create_access_token(
            {
                "login": auth_code["login"],
                "name": user["name"],
            }
        )

        await request.app.state.oauth_repo.delete_code(code)

        return {
        "access_token": access_token,
        "token_type": "Bearer",
    }
