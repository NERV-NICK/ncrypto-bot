from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column 
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import BigInteger, String, PickleType

import os
import dotenv

dotenv.load_dotenv()

engine = create_async_engine(url=os.getenv("DB_URL"))

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(50))
    username: Mapped[str] = mapped_column(String(50))
    score: Mapped[int] = mapped_column(BigInteger)
    referrals: Mapped[list] = mapped_column(PickleType)
    referrer: Mapped[int] = mapped_column(BigInteger)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)