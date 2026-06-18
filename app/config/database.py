from sqlalchemy import create_engine


class DBConfig:
    def __init__(self, db_user: str, db_password: str,
                 db_host: str, db_port: int, db_name: str):
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name

        self.DATABASE_URL = (
            f"postgresql+psycopg://"
            f"{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}"
            f"/{self.db_name}"
        )

        self.engine = create_engine(self.DATABASE_URL, pool_pre_ping=True)
