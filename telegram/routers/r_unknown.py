from __future__ import annotations
from loguru import logger

from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from telegram.courier import send_text
from telegram.texts.t_unknown import cmd_dict

router = Router()


@router.message()
@logger.catch
async def unknown(message: types.Message, state: FSMContext) -> None:
  logger.warning(f"→ Got UNKNOWN '{message.text}' command from {message.from_user.id}@{message.chat.id}")
  try:
    await state.clear()
    await send_text(
      message=message,
      text=cmd_dict['info'],
      reply=True,
      markup=types.ReplyKeyboardRemove()
    )
  
  except BaseException as E:
    logger.error(E)
    await send_text(
      message=message,
      text=cmd_dict['error']
    )

  return None
