from __future__ import annotations
from loguru import logger

from datetime import date
from aiogram import Router, types
from aiogram.filters import Command

from database.classes import AccountantUser

from telegram.courier import send_text
from telegram.texts.t_savings import cmd_dict

router = Router()


@router.message(Command("savings"))
@logger.catch
async def cmd_savings(message: types.Message) -> None:
  logger.info(f"→ Got '{message.text}' command from {message.from_user.id}@{message.chat.id}")

  try:
    user = AccountantUser()
    user.id = message.from_user.id
    user_profile = await user.get_profile()
    if user_profile is None:
      raise Exception("Not a user here - profile is None")

    message_list = message.text.split()

    if len(message_list) < 2:
      await send_text(
        message=message,
        text=cmd_dict['info'].format(savings=user_profile.savings)
      )
    else:
      new_savings = int(
        message_list[1]
      )
      user_profile.savings = new_savings
      user_profile.start_dt = date.today()
      await user_profile.merge_profile()
      await send_text(
        message=message,
        text=cmd_dict['set'].format(savings=user_profile.savings)
      )

  except ValueError as E:
    logger.warning(E)
    await send_text(
      message=message,
      text=cmd_dict['wrong']
    )

  except BaseException as E:
    logger.error(E)
    await send_text(
      message=message,
      text=cmd_dict['error']
    )

  return None
