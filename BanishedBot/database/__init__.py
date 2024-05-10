import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# from sqlalchemy.ext.declarative import declarative_base

from BanishedBot.constant import SRC_DIR

database_file = f"{SRC_DIR}/database/database.db"
if not os.path.isfile(database_file):
    open(database_file, "a").close()

engine = create_async_engine(f"sqlite+aiosqlite:///{database_file}")
Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()
