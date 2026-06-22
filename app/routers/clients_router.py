from fastapi import APIRouter, Request
from schemas.clients import RegisterClientRequest

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.post("/register")
async def register_client(request: Request, data: RegisterClientRequest):
    """Маршрут для регистрации клиента"""

    return await request.app.state.clients_service.register_client(request, data.client_name)