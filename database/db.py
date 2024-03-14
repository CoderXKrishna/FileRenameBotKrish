import asyncio
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import InvalidRequestError
from typing import Optional

import os

from sample_config import Config


def start() -> sessionmaker:
    engine = create_async_engine(Config.DB_URI, future=True)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


BASE = declarative_base()
SESSION = start()

INSERTION_LOCK = asyncio.Event()


class CustomCaption(BASE):
    __tablename__ = "caption"

    id = sa.Column(sa.Integer, primary_key=True)
    caption = sa.Column(sa.String)

    def __init__(self, id: int, caption: str):
        self.id = id
        self.caption = caption


async def update_cap(id: int, caption: str) -> None:
    async with INSERTION_LOCK:
        async with SESSION() as session:
            cap = await session.get(CustomCaption, id)
            if not cap:
                cap = CustomCaption(id, caption)
                session.add(cap)
                await session.flush()
            else:
                session.delete(cap)
                cap = CustomCaption(id, caption)
                session.add(cap)
            await session.commit()


async def del_caption(id: int) -> None:
    async with INSERTION_LOCK:
        async with SESSION() as session:
            cap = await session.get(CustomCaption, id)
            if cap:
                session.delete(cap)
                await session.commit()


async def get_caption(id: int) -> Optional[CustomCaption]:
    async with SESSION() as session
