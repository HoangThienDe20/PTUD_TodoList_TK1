from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Hello To-Do"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./todos.db"
    JWT_SECRET_KEY: str = "change-this-secret-key"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
