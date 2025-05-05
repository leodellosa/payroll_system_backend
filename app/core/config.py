from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "FastAPI Payroll System"
    port: int = 8001
    database_url: str = "sqlite:///./db.sqlite3"
    secret_key: str = "default-secret-key"
    environment: str = "development"
    reload: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
