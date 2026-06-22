from sqlalchemy import text


class OAuthRepository:
    """Класс для работы с кодами авторизации"""

    def __init__(self, engine):
        self.engine = engine

    async def create_code(self, code: str, login: str, expires_at: str):
        """Метод, который добавялет код авторизации в бд"""

        async with self.engine.begin() as conn:
            await conn.execute(
                text("""
                    INSERT INTO oauth_codes (code, login, expires_at)
                    VALUES (
                        :code,
                        :login,
                        :expires_at
                    )
                """),
                {
                    "code": code,
                    "login": login,
                    "expires_at": expires_at,
                },
            )

    async def get_code(self, code: str):
        """Метод, который возвращает данные
         кода авторизации (логин, длительность)"""

        async with self.engine.begin() as conn:
            result = await conn.execute(
                text("""
                    SELECT login, expires_at
                    FROM oauth_codes
                    WHERE code = :code
                """),
                {"code": code},
            )

            return result.mappings().first()

    async def delete_code(self, code: str):
        """Метод, который удаляет код авторизации из бд"""

        async with self.engine.begin() as conn:
            await conn.execute(
                text("""
                    DELETE FROM oauth_codes
                        WHERE code = :code
                """),
                {"code": code},
            )