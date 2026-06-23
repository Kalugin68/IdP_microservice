from datetime import datetime, timedelta
from fastapi import HTTPException
from jwt import encode, decode
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from config import env


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
            raise HTTPException(
                status_code=401,
                detail="Token expired",
            )

        except InvalidTokenError:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
            )
