from __future__ import annotations
from loguru import logger

from database.engine import create_db_engine
from database.classes import AccountantBase


@logger.catch
async def create_metadata() -> bool:
  def_result = False

  try:
    db_engine = create_db_engine()
    if not db_engine or db_engine is None:
      raise Exception(f"db_engine is None")

    async with db_engine.begin() as db_channel:
      await db_channel.run_sync(AccountantBase.metadata.create_all)

    await db_engine.dispose()    

  except BaseException as E:
    logger.critical(f"Cannot create database metadata: '{E.__repr__()}' ({E})")
    raise

  else:
    def_result = True

  return def_result


if __name__ == "__main__":
  pass
