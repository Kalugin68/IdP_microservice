from fastapi import HTTPException
from uuid import uuid4
from datetime import datetime, timedelta

from models.data import users, clients, oauth_codes
from services.token_service import Token


class OauthService:

    def authentication(self, login: str, password: str):
        """Возвращает код авторизации"""
        user = users.get(login)

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Неверные учетные данные",
            )

        if user["password"] != password:
            raise HTTPException(
                status_code=401,
                detail="Неверный пароль",
            )

        code = str(uuid4())

        oauth_codes[code] = {
            "login": login,
            "expires_at": datetime.utcnow() + timedelta(minutes=5),
        }

        return {"authorization_code": code}

    def authorization(self, code: str, client_id: str):
        """Возвращает JWT-токен"""

        client = clients.get(client_id)

        if not client:
            raise HTTPException(
                status_code=404,
                detail="Неизвестный клиент"
            )

        auth_code = oauth_codes.get(code)

        if not auth_code:
            raise HTTPException(
                status_code=401,
                detail="Неверный код авторизации"
            )

        if auth_code["expires_at"] < datetime.utcnow():
            del oauth_codes[code]

            raise HTTPException(
                status_code=401,
                detail="Срок действия кода истек"
            )

        access_token = Token(client.get("client_secret"))

        return access_token.create_access_token(
            {
                "login": auth_code["login"],
                "name": users.get(auth_code["login"]).get("name"),
            }
        )

