from sqlalchemy import text


class DBInitService:
    @staticmethod
    async def init_db(engine):
        async with engine.begin() as conn:
            await conn.execute(
                text("""
                CREATE TABLE IF NOT EXISTS users
                (
                    id SERIAL PRIMARY KEY,
                    login VARCHAR(255) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    name VARCHAR(255) NOT NULL
                )
                     """))

            await conn.execute(
                text("""
                CREATE TABLE IF NOT EXISTS clients
                (
                    id SERIAL PRIMARY KEY,
                    client_name VARCHAR(255) NOT NULL,
                    client_id VARCHAR(255) UNIQUE NOT NULL,
                    client_secret VARCHAR(255) NOT NULL
                )
                """))

            await conn.execute(
                text("""
                CREATE TABLE IF NOT EXISTS oauth_codes
                (
                    code UUID PRIMARY KEY,
                    login VARCHAR(255) NOT NULL,
                    expires_at TIMESTAMP NOT NULL
                )
                """))

    @staticmethod
    async def seed_data(engine):
        async with engine.begin() as conn:
            await conn.execute(
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

            await conn.execute(
                text("""
                INSERT INTO clients(client_name, client_id, client_secret)
                VALUES 
                (
                    'notifications',
                    '36-mggwergtwe35-43633f',
                    'super-secret-key'
                )
                ON CONFLICT (client_id) DO NOTHING
                """))
