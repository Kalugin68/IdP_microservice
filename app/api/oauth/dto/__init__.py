from pydantic import BaseModel, Field


class AuthorizeRequest(BaseModel):
    login: str = Field(..., min_length=4)
    password: str = Field(..., min_length=4)


class TokenRequest(BaseModel):
    client_id: str = Field(..., min_length=1)
    client_secret: str
    authorization_code: str = Field(..., min_length=1)