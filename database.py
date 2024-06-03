from typing import AsyncGenerator

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.asyncio import (AsyncSession,
                                    create_async_engine, )
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import (DB_HOST,
                    DB_NAME,
                    DB_PASS,
                    DB_PORT,
                    DB_USER, )

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class Base(DeclarativeBase):
    pass


metadata = MetaData()


engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()




