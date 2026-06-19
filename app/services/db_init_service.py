from sqlalchemy import text


class DBInitService:

    @staticmethod
    def init_db(engine):
        """Метод, который создаёт таблицы"""

        with engine.begin() as conn:
            conn.execute(
                text("""
                CREATE TABLE IF NOT EXISTS users
                (
                    id SERIAL PRIMARY KEY,
                    login VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    name VARCHAR(255) NOT NULL
                )
                     """))

            conn.execute(
                text("""
                CREATE TABLE IF NOT EXISTS clients
                (
                    id SERIAL PRIMARY KEY,
                    client_id VARCHAR(255) UNIQUE NOT NULL,
                    client_secret VARCHAR(255) NOT NULL
                )
                """))

            conn.execute(
                text("""
                CREATE TABLE IF NOT EXISTS oauth_codes
                (
                    code UUID PRIMARY KEY,
                    login VARCHAR(255) NOT NULL,
                    expires_at TIMESTAMP NOT NULL
                )
                """))

    @staticmethod
    def seed_data(engine):
        """Метод для заполнения таблиц данными"""

        with engine.begin() as conn:
            conn.execute(
                text("""
                INSERT INTO users(login, password, name)
                VALUES 
                (
                    'admin',
                    '123456',
                    'Administrator'
                )
                ON CONFLICT (login) DO NOTHING
                """))

            conn.execute(
                text("""
                INSERT INTO clients(client_id, client_secret)
                VALUES 
                (
                    'notifications',
                    'super-secret-key'
                )
                ON CONFLICT (client_id) DO NOTHING
                """))
