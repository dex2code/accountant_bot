from __future__ import annotations
from loguru import logger

from aiogram import Router, types
from aiogram.filters import Command

from telegram.courier import send_text
from telegram.texts.t_report import cmd_dict

router = Router()


@router.message(Command("report"))
@logger.catch
async def cmd_report(message: types.Message) -> None:
  logger.info(f"→ Got '{message.text}' command from {message.from_user.id}@{message.chat.id}")
  await send_text(
    message=message,
    text=cmd_dict['tbd']
  )
  return None


if __name__ == "__main__":
  pass
