from datetime import datetime, timedelta
from fastapi import HTTPException
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
import base64

from config import env


class TokenManager:
    def __init__(self):
        self.algorithm = env.jwt_algorithm

        self.private_key = (
            f"-----BEGIN PRIVATE KEY-----\n"
            f"{base64.b64decode(env.jwt_private.encode("utf-8"))}\n"
            f"-----END PRIVATE KEY-----"
        )

        self.public_key = (
            f"-----BEGIN PUBLIC KEY-----\n"
            f"{base64.b64decode(env.jwt_public.encode("utf-8"))}\n"
            f"-----END PUBLIC KEY-----"
        )

    def generate(
        self,
        data: dict,
        ttl_minutes: int = 30,
        token_type: str = "access",
    ) -> str:

        payload = data.copy()
        payload.update(
            {
                "type": token_type,
                "iat": int(datetime.utcnow().timestamp()),
                "exp": datetime.utcnow() + timedelta(minutes=ttl_minutes),
            }
        )

        return jwt.encode(
            payload,
            self.private_key,
            algorithm=self.algorithm,
        )

    def decode(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                self.public_key,
                algorithms=[self.algorithm],
            )

        except ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Token expired",
            )

        except JWTError:
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
            )
