from uuid import uuid4
from api.client.dbi import create_client


class ClientService:
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
