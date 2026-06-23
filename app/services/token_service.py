from datetime import datetime, timedelta
from jose import jwt


class Token:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        self.algorithm = "HS256"

    def create_access_token(self, payload: dict):
        data = payload.copy()
        data["exp"] = datetime.utcnow() + timedelta(minutes=30)

        return jwt.encode(
                data,
                self.secret_key,
                algorithm=self.algorithm,
            )
