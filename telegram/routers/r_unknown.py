from __future__ import annotations
from loguru import logger

import app_config

from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import as_list, as_line

from telegram.courier import send_text


router = Router()


@router.message()
@logger.catch
async def cmd_unknown(message: types.Message, state: FSMContext) -> None:
  logger.warning(f"→ Got UNKNOWN '{message.text}' command from {message.from_user.id}@{message.chat.id}")

  t = as_line(" ⁉ Неизвестная команда")

  try:
    await state.clear()
    await send_text(
      message=message,
      text=t,
      reply=True,
      markup=types.ReplyKeyboardRemove()
    )
  
  except BaseException as E:
    logger.error(E)
    t = as_list(
      as_line(f" 🙀 Кажется, что-то пошло не так!"),
      as_line(f" ☝ Попробуйте начать с команды /start")
    )
    await send_text(message=message, text=t)

  return None
