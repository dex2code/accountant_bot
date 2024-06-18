from __future__ import annotations
from loguru import logger

from sqlalchemy import URL as sql_url
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine



@logger.catch
def create_db_engine(config: dict) -> AsyncEngine:
  def_result = None

  try:
    db_url = sql_url.create(
      drivername=config['scheme'],
      database=config['database_path'],
      query=config['query']
    )

    def_result = create_async_engine(url=db_url, echo=config['echo'])
  
  except BaseException as E:
     logger.critical(f"Cannot create database engine: '{E.__repr__()} ({E})'")
     raise
  
  return def_result


if __name__ == "__main__":
    pass
