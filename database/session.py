from __future__ import annotations
from loguru import logger

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker


@logger.catch
def create_db_session(db_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
  try:
    def_result = async_sessionmaker(db_engine, autoflush=True, expire_on_commit=False)
  except BaseException as E:
    logger.critical(f"Cannot create database session: '{E.__repr__()}' ({E})")
    raise
  
  return def_result


if __name__ == "__main__":
    pass
