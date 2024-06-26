from __future__ import annotations
from loguru import logger

from aiogram import Router, types
from aiogram.filters import CommandStart

from database.classes import AccountantUser
from telegram.courier import send_text

from telegram.texts.t_start import cmd_dict


router = Router()


@router.message(CommandStart())
@logger.catch
async def cmd_start(message: types.Message) -> None:
  logger.info(f"→ Got '{message.text}' command from {message.from_user.id}@{message.chat.id}")

  try:
    await send_text(
      message=message,
      text=cmd_dict['hello'],
      reply=True,
      markup=types.ReplyKeyboardRemove()
    )

    user = AccountantUser()
    user.id = message.from_user.id
    user_profile = await user.get_profile()

    if user_profile is None:
      await user.create_profile()
      await send_text(
        message=message,
        text=cmd_dict['about']
      )

    await send_text(
      message=message,
      text=cmd_dict['help']
    )
    await send_text(
      message=message,
      text=cmd_dict['clue']
    )

  except BaseException as E:
    logger.error(E)
    await send_text(
      message=message,
      text=cmd_dict['error']
    )

  return None
