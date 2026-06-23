from uuid import uuid4


class ClientService:
    async def register_client(self, request, client_name):
        client_id = str(uuid4())
        client_secret = str(uuid4())

        await request.app.state.client_repo.create_client(
            client_id=client_id,
            client_secret=client_secret,
            client_name=client_name
        )

        return {
            "client_id": client_id,
            "client_secret": client_secret,
        }
