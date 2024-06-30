from __future__ import annotations
from loguru import logger
import app_config

import asyncio
from aiogram import Dispatcher

from database.metadata import create_metadata
from telegram.bot import get_telegram_api_key, create_telegram_bot, get_bot_commands

from telegram.routers import r_cancel
from telegram.routers import r_start
from telegram.routers import r_income
from telegram.routers import r_goal
from telegram.routers import r_report
from telegram.routers import r_spending
from telegram.routers import r_reset
from telegram.routers import r_unknown


@logger.catch
async def main() -> None:
  logger.info("*** Starting Accountant Bot...")

  try:
    await create_metadata()

    telegram_api_key = get_telegram_api_key()
    telegram_bot_commands = get_bot_commands()
    telegram_bot = await create_telegram_bot(api_key=telegram_api_key)
    if not await telegram_bot.set_my_commands(
      commands=telegram_bot_commands,
      request_timeout=app_config.telegram['timeout_sec'],
    ): raise Exception("Cannot set bot commands")
    logger.info(f"{telegram_bot=}")

    telegram_dispatcher = Dispatcher()
    telegram_dispatcher.include_router(router=r_cancel.router)
    telegram_dispatcher.include_router(router=r_start.router)
    telegram_dispatcher.include_router(router=r_income.router)
    telegram_dispatcher.include_router(router=r_goal.router)
    telegram_dispatcher.include_router(router=r_report.router)
    telegram_dispatcher.include_router(router=r_spending.router)
    telegram_dispatcher.include_router(router=r_reset.router)
    telegram_dispatcher.include_router(router=r_unknown.router)
    logger.info(f"{telegram_dispatcher=}")
    await telegram_dispatcher.start_polling(telegram_bot)

  except BaseException as E:
    logger.critical(f"Exception found: '{E.__repr__()}' ({E})")
    raise

  finally:
    logger.info(f"*** Shutdown Accountant bot")
    await telegram_dispatcher.emit_shutdown()

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
