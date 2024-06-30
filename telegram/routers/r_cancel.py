from __future__ import annotations
from loguru import logger

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from telegram.courier import send_text

from telegram.texts.t_cancel import cmd_dict


router = Router()


@router.message(Command("cancel"))
@logger.catch
async def cmd_cancel(message: types.Message, state: FSMContext) -> None:
  logger.info(f"→ Got '{message.text}' command from {message.from_user.id}@{message.chat.id}")

  try:
    await state.clear()
    await send_text(
      message=message,
      text=cmd_dict['cancel'],
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


if __name__ == "__main__":
  pass
