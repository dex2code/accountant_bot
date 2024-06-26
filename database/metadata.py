from __future__ import annotations
from loguru import logger

from database.engine import create_db_engine
from database.classes import AccountantBase


@logger.catch
async def create_metadata() -> None:
  try:
    db_engine = create_db_engine()
    async with db_engine.begin() as db_channel:
      await db_channel.run_sync(AccountantBase.metadata.create_all)
  except BaseException as E:
    logger.critical(E)
    raise
  finally:
    await db_engine.dispose()
  return None


if __name__ == "__main__":
  pass
