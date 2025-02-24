import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Загружаем переменные из .env файла
load_dotenv()

# Получаем URL для подключения к базе данных из .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Создаем движок для асинхронного подключения
engine = create_async_engine(DATABASE_URL, echo=True)

# Сессия для работы с базой данных
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Базовый класс для моделей
Base = declarative_base()
