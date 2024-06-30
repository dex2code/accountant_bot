from __future__ import annotations
from loguru import logger

from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.classes import AccountantUser
from telegram.texts.t_reset import cmd_dict, confirm_message

from telegram.courier import send_text


class ResetState(StatesGroup):
    reset_sure = State()

router = Router()


@router.message(Command("reset"))
@logger.catch
async def cmd_reset(message: types.Message, state: FSMContext) -> None:
  logger.info(f"→ Got '{message.text}' command from {message.from_user.id}@{message.chat.id}")

  try:
    user = AccountantUser()
    user.id = message.from_user.id
    user_profile = await user.get_profile()
    if user_profile is None:
      raise Exception("Not a user here - profile is None")
    
    await send_text(
      message=message,
      text=cmd_dict['confirm']
    )
    await state.set_state(ResetState.reset_sure)
  
  except BaseException as E:
    logger.error(E)
    await state.clear()

  return None


@router.message(ResetState.reset_sure, F.text)
@logger.catch
async def do_reset(message: types.Message, state: FSMContext) -> None:
  logger.info(f"→ Got '{message.text}' command from {message.from_user.id}@{message.chat.id}")

  try:
    user = AccountantUser()
    user.id = message.from_user.id
    user_profile = await user.get_profile()
    if user_profile is None:
      raise Exception("Not a user here - profile is None")

    await state.clear()

    if message.text.upper() != confirm_message.upper():
      await send_text(
        message=message,
        text=cmd_dict['cancel']
      )
      return None
    
    await user_profile.reset_profile()
    await send_text(
      message=message,
      text=cmd_dict['done']
    )
  
  except BaseException as E:
    logger.error(E)
    await state.clear()
    await send_text(
      message=message,
      text=cmd_dict['error']
    )

  return None


if __name__ == "__main__":
  pass
