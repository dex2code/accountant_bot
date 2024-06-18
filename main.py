from __future__ import annotations

import asyncio

import app_config
from database.engine import create_db_engine
from database.init import create_metadata
from telegram.dispatcher import create_telegram_dispatcher
from telegram.bot import create_telegram_bot


from loguru import logger


@logger.catch
async def main() -> None:

  db_engine = create_db_engine(config=app_config.database)
  if db_engine is None:
    raise Exception(f"db_engine is None")
  
  metadata_result = await create_metadata(db_engine=db_engine)
  if not metadata_result:
    raise Exception(f"Create database metadata failed")

  telegram_dispatcher = create_telegram_dispatcher()
  telegram_bot = await create_telegram_bot()

  return None


if __name__ == "__main__":
  logger.add(
    sink=app_config.log['path'],
    level=app_config.log['level'],
    format=app_config.log['format'],
    backtrace=app_config.log['backtrace'],
    diagnose=app_config.log['diagnose'],
    enqueue=app_config.log['enqueue'],
    rotation=app_config.log['rotation'],
    retention=app_config.log['retention'],
    compression=app_config.log['compression']
  )

  asyncio.run(main=main())
