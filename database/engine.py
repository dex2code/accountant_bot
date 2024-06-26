from __future__ import annotations
from loguru import logger
import app_config

from sqlalchemy import URL as sql_url
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine


@logger.catch
def create_db_engine() -> AsyncEngine:
  try:
    db_url = sql_url.create(
      drivername=app_config.database['scheme'],
      database=app_config.database['path'],
      query=app_config.database['query']
    )
    db_engine = create_async_engine(url=db_url, echo=app_config.database['echo'])
  except BaseException as E:
     logger.critical(E)
     raise
  return db_engine


if __name__ == "__main__":
    pass
