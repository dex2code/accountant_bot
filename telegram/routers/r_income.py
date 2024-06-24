from __future__ import annotations
from loguru import logger

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import as_list, as_line, Italic

from database.classes import AccountantUser
from telegram.courier import send_text


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
      t = as_list(
        as_line(f" 💵 ⋅ Ваш указанный ежемесячный доход: {user_profile.monthly_income:,}"),
        as_line(
          f"☝ Чтобы установить новое значение,\n",
          f"пришлите /income ", Italic("<значение>"), "\n",
          f"Например: /income ", Italic("1200"))
      )
      await send_text(message=message, text=t)

    else:
      new_income = int(
        message_list[1]
      )
      user_profile.monthly_income = new_income
      if not await user_profile.merge_profile():
        raise Exception("Cannot merge user profile")
      t = as_list(
        as_line(f" 🥳 Отлично, ежемесячный доход установлен: {user_profile.monthly_income:,}"),
        as_line(f" ☝ Возможно, теперь вы хотите указать размер ваших текущих накоплений? Команда /savings")
      )
      await send_text(message=message, text=t)

  except ValueError as E:
    logger.warning(E)
    t = as_list(
      as_line(
        f" 🤔 Кажется, вы ввели значение, которое я не могу понять.\n",
        f"Попробуйте еще раз, указав только цифры."
      )
    )
    await send_text(message=message, text=t)

  except BaseException as E:
    logger.error(E)
    t = as_list(
      as_line(f" 🙀 Кажется, что-то пошло не так!"),
      as_line(f" ☝ Попробуйте начать с команды /start")
    )
    await send_text(message=message, text=t)

  return None
