from __future__ import annotations
from loguru import logger

from datetime import date
from aiogram import Router, types, F

from database.classes import AccountantUser, AccountantOperations

from app_tools import get_month_days

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

    today = date.today()
    sum_today_spendings = await user_profile.get_sum_date_spendings(d=today)
    sum_month_spendings = await user_profile.get_sum_month_spendings(
      y=int(today.strftime("%Y")),
      m=int(today.strftime("%-m"))
    )
    await send_text(
      message=message,
      text=cmd_dict['spent'].format(
        operation_value=operation.operation_value,
        sum_month_spendings=sum_month_spendings,
        sum_today_spendings=sum_today_spendings,
      )
    )

    left_spends = user_profile.monthly_income - user_profile.monthly_goal - sum_month_spendings
    if left_spends > 0:
      left_days_month = get_month_days()['left_days_month']
      avg_spends = int(
        left_spends / left_days_month
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
      overspent = sum_month_spendings - (user_profile.monthly_income - user_profile.monthly_goal)
      left_income = user_profile.monthly_income - sum_month_spendings
      await send_text(
        message=message,
        text=cmd_dict['info_negative'].format(
          monthly_goal=user_profile.monthly_goal,
          sum_monthly_spendings=sum_month_spendings,
          overspent=overspent,
          left_income=left_income
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
