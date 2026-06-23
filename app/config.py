from pydantic_settings import BaseSettings, SettingsConfigDict


class Env(BaseSettings):
    jwt_private: str
    jwt_public: str
    jwt_algorithm: str

    db_dsn: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

env = Env()