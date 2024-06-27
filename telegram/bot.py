from __future__ import annotations
from loguru import logger

from os import getenv as os_getenv
from dotenv import load_dotenv

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand


@logger.catch
def get_telegram_api_key() -> str:
  if not load_dotenv():
    raise Exception(f"Cannot load dotenv")

  telegram_key = os_getenv("ACCOUNTANT_TG_KEY")
  if not telegram_key or telegram_key is None:
    raise Exception(f"ACCOUNTANT_TG_KEY not found in .env")

  return telegram_key  


@logger.catch
async def create_telegram_bot(api_key: str) -> Bot:
  telegram_bot = Bot(
    token=api_key,
    default=DefaultBotProperties(
      parse_mode=ParseMode.HTML,
      link_preview_is_disabled=True
    )
  )

  if not telegram_bot or telegram_bot is None:
    raise Exception(f"Cannot create Telegram Bot")
  
  return telegram_bot


@logger.catch
def get_bot_commands() -> list[BotCommand]:
  bot_commands = [
    BotCommand(command="/report", description="📊 ⋅ Отчет за месяц"),
    BotCommand(command="/income", description="💵 ⋅ Ежемесячный доход"),
    BotCommand(command="/goal", description="🎯 ⋅ Ежемесячная цель"),
    BotCommand(command="/reset", description="⭕️ ⋅ Сбросить данные профиля"),
  ]

  return bot_commands


if __name__ == "__main__":
  pass
