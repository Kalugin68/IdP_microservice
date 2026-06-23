from fastapi import HTTPException
from uuid import uuid4
from datetime import datetime, timedelta

from api.oauth.dbi import (
    get_auth_code, get_user_by_login, get_client_by_client_id,
    delete_auth_code, create_auth_code
)


class OauthService:
    async def authentication(self, login: str, password: str):
        user = await get_user_by_login(login)

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials",
            )

        if user.password != password:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials",
            )

        code = str(uuid4())
        expires_at = datetime.utcnow() + timedelta(minutes=5)

        await create_auth_code(code, login, expires_at)

        return {"authorization_code": code}

    async def authorization(self, request, code: str, client_id: str,
                      client_secret: str):
        client = await get_client_by_client_id(client_id)

        if not client:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        if client.client_secret != client_secret:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        auth_code = await get_auth_code(code)

        if not auth_code:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        if auth_code.expires_at < datetime.utcnow():
            await delete_auth_code(code)

            raise HTTPException(
                status_code=401,
                detail="The code has expired"
            )

        user = await get_user_by_login(auth_code.login)

        access_token = request.app.state.token_manager.generate(
            {
                "sub": auth_code.login,
                "name": user.name,
                "client_id": client_id,
            }
        )

        await delete_auth_code(code)

        return {
        "access_token": access_token,
        "token_type": "Bearer",
    }
