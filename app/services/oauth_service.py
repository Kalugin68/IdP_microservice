from fastapi import HTTPException
from uuid import uuid4
from datetime import datetime, timedelta

from models.data import users, clients, oauth_codes



class OauthService:
    """Класс для работы с авторизацией и аутентификацией"""

    def authentication(self, request, login: str, password: str):
        """Возвращает код авторизации"""

        user = request.app.state.user_repo.get_by_login(login)

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

        request.app.state.oauth_repo.create_code(code, login, expires_at)

        return {"authorization_code": code}

    def authorization(self, request, code: str, client_id: str,
                      client_secret: str):
        """Возвращает JWT-токен"""

        client = request.app.state.client_repo.get_by_client_id(client_id)

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

        auth_code = request.app.state.oauth_repo.get_code(code)

        if not auth_code:
            raise HTTPException(
                status_code=401,
                detail="Неверные данные"
            )

        if auth_code["expires_at"] < datetime.utcnow():
            request.app.state.oauth_repo.delete_code(code)

            raise HTTPException(
                status_code=401,
                detail="Срок действия кода истек"
            )

        name = request.app.state.user_repo.get_by_login(auth_code["login"]).get("name")

        access_token = request.app.state.token_service.create_access_token(
            {
                "login": auth_code["login"],
                "name": name,
            }
        )

        request.app.state.oauth_repo.delete_code(code)

        return {
        "access_token": access_token,
        "token_type": "Bearer",
    }
