from __future__ import annotations

from os import getenv as os_getenv
from dotenv import load_dotenv

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


def get_telegram_api_key() -> str:
  if not load_dotenv():
    raise Exception(f"Cannot load dotenv")

  telegram_key = os_getenv("ACCOUNTANT_TG_KEY")
  if not telegram_key:
    raise Exception(f"ACCOUNTANT_TG_KEY not found in .env")

  return telegram_key  


async def create_telegram_bot() -> Bot:
  return Bot(
    token=get_telegram_api_key(),
    default=DefaultBotProperties(
      parse_mode=ParseMode.HTML,
      link_preview_is_disabled=True
    )
  )


if __name__ == "__main__":
  pass
