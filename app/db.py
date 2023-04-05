"""Модуль для инициализации подключения к БД."""
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
)

async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

