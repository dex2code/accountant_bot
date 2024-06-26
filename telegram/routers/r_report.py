from __future__ import annotations
from loguru import logger

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.formatting import as_list, as_line, Italic, Underline

from database.classes import AccountantUser
from telegram.courier import send_text


router = Router()


@router.message(Command("report"))
@logger.catch
async def cmd_report(message: types.Message) -> None:
  logger.info(f"→ Got '{message.text}' command from {message.from_user.id}@{message.chat.id}")
  return None