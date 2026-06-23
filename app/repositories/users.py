from sqlalchemy import text


class UserRepository:
    def __init__(self, engine):
        self.engine = engine

    async def get_by_login(self, login: str):
        async with self.engine.begin() as conn:
            result = await conn.execute(
                text("""
                    SELECT login, password, name
                    FROM users
                    WHERE login = :login
                """),
                {"login": login},
            )

            return result.mappings().first()