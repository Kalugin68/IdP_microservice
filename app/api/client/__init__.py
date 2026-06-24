from fastapi import APIRouter, Request

from .dto import RegisterClientRequest


router = APIRouter(prefix="/clients", tags=["Clients"])


@router.post("/register")
async def register_client(request: Request, data: RegisterClientRequest):
    return await request.app.state.oauth_service.register_client(data.client_name)