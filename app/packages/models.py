import os

from sqlalchemy import String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "12345")
POSTGRES_DB = os.getenv("POSTGRES_DB", "persons_swapi")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")

PG_DSN = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


class Person(Base):
    __tablename__ = 'persons'

    id: Mapped[int] = mapped_column(primary_key=True)
    birth_year: Mapped[str] = mapped_column(String(50), nullable=True)
    eye_color: Mapped[str] = mapped_column(String(50), nullable=True)
    films: Mapped[str] = mapped_column(String(), nullable=True)
    gender: Mapped[str] = mapped_column(String(50), nullable=True)
    hair_color: Mapped[str] = mapped_column(String(50), nullable=True)
    height: Mapped[str] = mapped_column(String(50), nullable=True)
    homeworld: Mapped[str] = mapped_column(String(100), nullable=True)
    mass: Mapped[str] = mapped_column(String(50), nullable=True)
    name: Mapped[str] = mapped_column(String(50), nullable=True)
    skin_color: Mapped[str] = mapped_column(String(50), nullable=True)
    species: Mapped[str] = mapped_column(String(), nullable=True)
    starships: Mapped[str] = mapped_column(String(), nullable=True)
    vehicles: Mapped[str] = mapped_column(String(), nullable=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
