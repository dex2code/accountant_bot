from __future__ import annotations
from loguru import logger
import app_config

import asyncio

from database.engine import create_db_engine
from database.init import create_metadata
from telegram.dispatcher import create_telegram_dispatcher
from telegram.bot import get_telegram_api_key, create_telegram_bot, get_bot_commands


@logger.catch
async def main() -> None:
  logger.info("*** Starting Accountant Bot...")

  try:
    db_engine = create_db_engine(config=app_config.database)
    if not db_engine or db_engine is None:
      raise Exception(f"db_engine is None")
    logger.info(f"{db_engine=}")

    metadata_result = await create_metadata(db_engine=db_engine)
    if not metadata_result:
      raise Exception(f"Create database metadata failed")
    logger.info(f"{metadata_result=}")
  
    telegram_dispatcher = create_telegram_dispatcher()
    logger.info(f"{telegram_dispatcher=}")
  
    telegram_api_key = get_telegram_api_key()
    telegram_bot = await create_telegram_bot(api_key=telegram_api_key)
    logger.info(f"{telegram_bot=}")

    telegram_bot_commands = get_bot_commands()
    if not await telegram_bot.set_my_commands(
      commands=telegram_bot_commands,
      request_timeout=app_config.telegram['timeout_sec'],
    ):
      raise Exception("Cannot set bot commands")
    logger.info(f"{telegram_bot_commands=}")

    await telegram_bot.delete_webhook(drop_pending_updates=True)
    logger.info("Starting bot polling...")
    await telegram_dispatcher.start_polling(
      telegram_bot,
      skip_updates=True,
    )

  except BaseException as E:
    logger.critical(f"Exception found: '{E.__repr__()}' ({E})")
    raise

  finally:
    await db_engine.dispose()
    await telegram_dispatcher.emit_shutdown()
    logger.info(f"*** Shutdown Accountant bot")

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
