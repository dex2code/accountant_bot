from __future__ import annotations
from loguru import logger

import calendar
from datetime import datetime

from aiogram import Router, types, F

from database.classes import AccountantUser, AccountantOperations

from telegram.courier import send_text
from telegram.texts.t_spending import cmd_dict


router = Router()


@router.message(F.text.regexp(r"^(\d+)$"))
@logger.catch
async def cmd_spending(message: types.Message) -> None:
  logger.info(f"→ Got '{message.text}' command from {message.from_user.id}@{message.chat.id}")

  try:
    user = AccountantUser()
    user.id = message.from_user.id
    user_profile = await user.get_profile()
    if user_profile is None:
      raise Exception("Not a user here - profile is None")

    new_spending_value = int(message.text)
    operation = AccountantOperations()
    operation.user_id = message.from_user.id
    operation.operation_value = new_spending_value
    await operation.create_operation()
    sum_daily_spendings = await user_profile.get_sum_daily_spendings()
    await send_text(
      message=message,
      text=cmd_dict['spent'].format(
        operation_value=operation.operation_value,
        sum_daily_spendings=sum_daily_spendings
      )
    )

    sum_monthly_spendings = await user_profile.get_sum_monthly_spendings()
    left_spends = user_profile.monthly_income - user_profile.monthly_goal - sum_monthly_spendings

    if left_spends > 0:
      day_in_month = calendar.monthrange(year=datetime.today().year, month=datetime.today().month)[1]
      left_month = day_in_month - datetime.today().day + 1
      avg_spends = int(
        left_spends / left_month
      )
      await send_text(
        message=message,
        text=cmd_dict['info_positive'].format(
          monthly_goal=user_profile.monthly_goal,
          left_spends=left_spends,
          avg_spends=avg_spends
        )
      )

    else:
      diff_spend = sum_monthly_spendings - (user_profile.monthly_income - user_profile.monthly_goal)
      left_month = user_profile.monthly_income - sum_monthly_spendings
      await send_text(
        message=message,
        text=cmd_dict['info_negative'].format(
          monthly_goal=user_profile.monthly_goal,
          sum_monthly_spendings=sum_monthly_spendings,
          diff_spend=diff_spend,
          left_month=left_month
        )
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
