from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    debug: bool = False
    secret_key: str = "your-secret-key-change-in-production"
    db_name: str = "dbname"
    db_user: str = "user"
    db_password: str = "password"
    db_host: str = "localhost"
    db_port: int = 5432

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
