from uuid import uuid4

from sqlalchemy import text


class ClientRepository:
    """Класс для работы с клиентами"""

    def __init__(self, engine):
        self.engine = engine

    def get_by_client_id(self, client_id: str):
        """Метод, который возвращает клиента по его id"""

        with self.engine.begin() as conn:
            result = conn.execute(
                text("""
                     SELECT client_name, client_id, client_secret
                     FROM clients
                     WHERE client_id = :client_id
                """),
                {"client_id": client_id},
            )

            return result.mappings().first()

    def create_client(self, client_name: str, client_id: str, client_secret: str):
        """Метод, который добавляет клиента в бд"""

        with self.engine.begin() as conn:
            conn.execute(
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