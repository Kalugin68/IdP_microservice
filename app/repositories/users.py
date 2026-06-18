from sqlalchemy import text
from config.database import DBConfig


class UserRepository:
    """Класс для работы с пользователями"""

    def __init__(self, engine):
        self.engine = engine

    def get_by_login(self, login: str):
        """Метод, который возвращает данные пользователя по его логину"""

        with self.engine.begin() as conn:
            result = conn.execute(
                text("""
                    SELECT login, password, name
                    FROM users
                    WHERE login = :login
                """),
                {"login": login},
            )

            return result.mappings().first()