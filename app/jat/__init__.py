from datetime import datetime

from fastapi import Request
from fastapi.security import HTTPBearer
from jwt import encode, decode
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from config import env
from exceptions import ServiceException


class TokenManager:
    def __init__(self):
        self.algorithm = env.jwt_algorithm

        self.private_key = (
            f"-----BEGIN PRIVATE KEY-----\n"
            f"{env.jwt_private}\n"
            f"-----END PRIVATE KEY-----"
        )

        self.public_key = (
            f"-----BEGIN PUBLIC KEY-----\n"
            f"{env.jwt_public}\n"
            f"-----END PUBLIC KEY-----"
        )

    def generate(
        self,
        data: dict,
        ttl: int = 30,
        token_type: str = "access",
    ) -> str:

        payload = data.copy()
        payload.update(
            {
                "type": token_type,
                "iat": int(datetime.now().timestamp()),
                "exp": int(datetime.now().timestamp()) + ttl,
            }
        )

        return encode(
            payload,
            self.private_key,
            algorithm=self.algorithm,
        )

    def decode(self, token: str) -> dict:
        try:
            return decode(
                token,
                self.public_key,
                algorithms=[self.algorithm],
            )

        except ExpiredSignatureError:
            raise ServiceException(
                status_code=401,
                msg="Token expired",
            )

        except InvalidTokenError as e:
            raise ServiceException(
                status_code=401,
                msg=f"Invalid token: {e}",
            )

        except Exception:
            raise ServiceException(
                status_code=401,
                msg="Invalid token"
            )


class bearer_t(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        self.credentials = auth.credentials

        self.data = request.app.state.token_manager.decode(auth.credentials)

        return self

