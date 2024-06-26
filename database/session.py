from __future__ import annotations
from loguru import logger
import app_config

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker


@logger.catch
def create_db_session(db_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
  try:
    db_session = async_sessionmaker(
      db_engine,
      autoflush=app_config.database['autoflush'],
      expire_on_commit=app_config.database['expire_on_commit']
    )
  except BaseException as E:
    logger.critical(f"Cannot create database session: '{E.__repr__()}' ({E})")
    raise
  return db_session


if __name__ == "__main__":
    pass
