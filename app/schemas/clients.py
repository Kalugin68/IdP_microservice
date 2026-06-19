from pydantic import BaseModel, Field


class RegisterClientRequest(BaseModel):
    client_name: str = Field(..., min_length=1)
