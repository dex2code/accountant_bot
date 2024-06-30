from __future__ import annotations
from loguru import logger

from aiogram import Router, types
from aiogram.filters import Command

from database.classes import AccountantUser

from telegram.courier import send_text
from telegram.texts.t_income import cmd_dict

router = Router()


@router.message(Command("income"))
@logger.catch
async def cmd_income(message: types.Message) -> None:
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
        text=cmd_dict['info'].format(monthly_income=user_profile.monthly_income)
      )

    else:
      new_income = int(
        message_list[1]
      )

      if new_income <= user_profile.monthly_goal:
        await send_text(
          message=message,
          text=cmd_dict['less'].format(monthly_goal=user_profile.monthly_goal)
        )
        return None

      user_profile.monthly_income = new_income
      await user_profile.merge_profile()
      await send_text(
        message=message,
        text=cmd_dict['set'].format(monthly_income=user_profile.monthly_income)
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
      message=message,text=cmd_dict['error']
    )

  return None


if __name__ == "__main__":
  pass
