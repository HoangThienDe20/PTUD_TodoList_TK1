from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Hello To-Do"
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./todos.db"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
