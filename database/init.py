from __future__ import annotations
from loguru import logger

from sqlalchemy.ext.asyncio import AsyncEngine

from database.classes import AccountantBase


@logger.catch
async def create_metadata(db_engine: AsyncEngine) -> bool:
  def_result = False

  try:
    async with db_engine.begin() as db_connection:
      await db_connection.run_sync(AccountantBase.metadata.create_all)

  except BaseException as E:
    logger.critical(f"Cannot create database metadata: '{E.__repr__()}' ({E})")
    raise

  else:
    logger.info(f"Database metadata successfully created")
    def_result = True

  return def_result


if __name__ == "__main__":
  pass
