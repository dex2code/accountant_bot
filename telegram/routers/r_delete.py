from __future__ import annotations
from loguru import logger

from datetime import date
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database.classes import AccountantUser
from telegram.texts.t_delete import cmd_dict, confirm_message

from telegram.courier import send_text


class DeleteState(StatesGroup):
    delete_sure = State()

router = Router()


@router.message(Command("delete"))
@logger.catch
async def cmd_delete(message: types.Message, state: FSMContext) -> None:
  logger.info(f"→ Got '{message.text}' command from {message.from_user.id}@{message.chat.id}")

  try:
    user = AccountantUser()
    user.id = message.from_user.id
    user_profile = await user.get_profile()
    if user_profile is None:
      raise Exception("Not a user here - profile is None")
    
    last_spending = await user_profile.get_last_spending()
    if last_spending is None:
      await send_text(
        message=message,
        text=cmd_dict['no_spendings']
      )
      return None
    
    await send_text(
      message=message,
      text=cmd_dict['confirm'].format(
        last_spend_value=last_spending.operation_value,
        last_spend_date=last_spending.operation_dt.strftime("%d.%m.%y"),
        last_spend_time=last_spending.operation_tt.strftime("%H:%M")
      )
    )
    await state.set_state(DeleteState.delete_sure)
  
  except BaseException as E:
    logger.error(E)
    await state.clear()

  return None


@router.message(DeleteState.delete_sure, F.text)
@logger.catch
async def do_delete(message: types.Message, state: FSMContext) -> None:
  logger.info(f"→ Got '{message.text}' command from {message.from_user.id}@{message.chat.id}")

  try:
    user = AccountantUser()
    user.id = message.from_user.id
    user_profile = await user.get_profile()
    if user_profile is None:
      raise Exception("Not a user here - profile is None")

    await state.clear()

    last_spending = await user_profile.get_last_spending()
    if last_spending is None:
      await send_text(
        message=message,
        text=cmd_dict['no_spendings']
      )
      return None

    if message.text.upper() != confirm_message.upper():
      await send_text(
        message=message,
        text=cmd_dict['cancel']
      )
      return None
    
    await last_spending.delete_operation()
    await send_text(
      message=message,
      text=cmd_dict['done'].format(
        sum_daily_spendings=await user_profile.get_sum_date_spendings(d=date.today())
      )
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
