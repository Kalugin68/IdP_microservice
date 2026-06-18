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
                     SELECT client_id, client_secret
                     FROM clients
                     WHERE client_id = :client_id
                """),
                {"client_id": client_id},
            )

            return result.mappings().first()