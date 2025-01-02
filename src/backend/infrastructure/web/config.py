import os

class Settings:
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "your_username")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "your_password")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "your_database")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    
    DATABASE_URL: str = (
        f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

settings = Settings()
