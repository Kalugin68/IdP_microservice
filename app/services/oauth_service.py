from fastapi import HTTPException
from uuid import uuid4
from datetime import datetime, timedelta

from api.oauth.dbi import get_user_by_login, get_client_by_client_id
from api.client.dbi import create_client
from exceptions import ServiceException


class OauthService:
    async def authentication(self, request, login: str, password: str):
        user = await get_user_by_login(login)

        if not user:
            raise ServiceException(
                status_code=401,
                msg="Invalid credentials",
            )

        if user.password != password:
            raise ServiceException(
                status_code=401,
                msg="Invalid credentials",
            )

        code = str(uuid4())

        request.app.state.auth_codes[code] = {
            "login": login
        }

        return {"authorization_code": code}

    async def authorization(self, request, code: str, client_id: str,
                      client_secret: str):
        client = await get_client_by_client_id(client_id)

        if not client:
            raise ServiceException(
                status_code=401,
                msg="Invalid credentials"
            )

        if client.client_secret != client_secret:
            raise ServiceException(
                status_code=401,
                msg="Invalid credentials"
            )

        auth_code = request.app.state.auth_codes.get(code)

        if not auth_code:
            raise ServiceException(
                status_code=401,
                msg="Invalid credentials"
            )

        user = await get_user_by_login(auth_code["login"])

        access_token = request.app.state.token_manager.generate(
            {
                "sub": auth_code["login"],
                "name": user.name,
                "client_id": client_id,
            }
        )

        request.app.state.auth_codes.pop(code, None)

        return {
        "access_token": access_token,
        "token_type": "Bearer",
    }

    async def register_client(self, client_name):
        client_id = str(uuid4())
        client_secret = str(uuid4())

        await create_client(
            client_id=client_id,
            client_secret=client_secret,
            client_name=client_name
        )

        return {
            "client_id": client_id,
            "client_secret": client_secret,
        }
