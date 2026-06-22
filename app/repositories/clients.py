from uuid import uuid4

from sqlalchemy import text


class ClientRepository:
    """Класс для работы с клиентами"""

    def __init__(self, engine):
        self.engine = engine

    async def get_by_client_id(self, client_id: str):
        """Метод, который возвращает клиента по его id"""

        async with self.engine.begin() as conn:
            result = await conn.execute(
                text("""
                     SELECT client_name, client_id, client_secret
                     FROM clients
                     WHERE client_id = :client_id
                """),
                {"client_id": client_id},
            )

            return result.mappings().first()

    async def create_client(self, client_name: str, client_id: str, client_secret: str):
        """Метод, который добавляет клиента в бд"""

        async with self.engine.begin() as conn:
            await conn.execute(
                text("""
                INSERT INTO clients (client_name, client_id, client_secret)
                VALUES 
                (
                    :client_name,
                    :client_id,
                    :client_secret
                )
                """),
                {
                    "client_name": client_name,
                    "client_id": client_id,
                    "client_secret": client_secret,
                },
            )