from __future__ import annotations
from loguru import logger

from datetime import date, timedelta
from aiogram import Router, types
from aiogram.filters import Command
from quickchart import QuickChart

from telegram.courier import send_text
from telegram.texts.t_report import cmd_dict

from database.classes import AccountantUser, AccountantOperation
from app_tools import get_month_days


router = Router()


@router.message(Command("report"))
@logger.catch
async def cmd_report(message: types.Message) -> None:
  logger.info(f"→ Got '{message.text}' command from {message.from_user.id}@{message.chat.id}")

  try:
    user = AccountantUser()
    user.id = message.from_user.id
    user_profile = await user.get_profile()
    if user_profile is None:
      raise Exception("Not a user here - profile is None")

    today = date.today()
    today_str = today.strftime("%-d %b %Y")

    today_spent = await user_profile.get_sum_date_spendings(d=today)
    today_spendings = await user_profile.get_date_spendings(d=today)

    list_spendings = ""
    operation: AccountantOperation
    for operation in today_spendings:
      list_spendings += f"\n ⋅ {operation.operation_value:,} ₽ в {operation.operation_tt.strftime('%H:%M')}"
    if not list_spendings:
      list_spendings = " нет трат"

    this_month_spent = await user_profile.get_sum_month_spendings(
      y=int(today.strftime("%Y")),
      m=int(today.strftime("%-m"))
    )

    first_day = today.replace(day=1)
    last_month = first_day - timedelta(days=1)
    last_month_spent = await user_profile.get_sum_month_spendings(
      y=int(last_month.strftime("%Y")),
      m=int(last_month.strftime("%-m"))
    )

    left_spends=(user_profile.monthly_income - user_profile.monthly_goal - this_month_spent)
    if left_spends < 0:
      left_spends = 0
    left_days_month = get_month_days()['left_days_month']
    avg_spends = int(
      left_spends / left_days_month
    )

    await send_text(
      message=message,
      text=cmd_dict['today_report'].format(
        today_str=today_str,
        today_spent=today_spent,
        today_spendings=list_spendings,
        this_month_spent=this_month_spent,
        last_month_spent=last_month_spent,
        user_goal=user_profile.monthly_goal,
        left_spends=left_spends,
        avg_spends=avg_spends
      )
    )

  except BaseException as E:
    logger.error(E)
    await send_text(
      message=message,
      text=cmd_dict['error']
    )

  try:
    user = AccountantUser()
    user.id = message.from_user.id
    user_profile = await user.get_profile()
    if user_profile is None:
      raise Exception("Not a user here - profile is None")

    chart_config = {
      "type": "line",
      "data": {
        "labels": [],
        "datasets": [
          {
            "label": 'Траты по дням, ₽',
            "data": [],
            "fill": False,
            "borderColor": "red",
          },
        ],
      },
    }

    today = date.today()
    month_agg = await user_profile.get_agg_month_spendings(
      y=int(today.strftime("%Y")),
      m=int(today.strftime("%-m"))
    )
    for agg in month_agg:
      chart_config['data']['labels'].append(agg[0].strftime("%-d %b %Y"))
      chart_config['data']['datasets'][0]['data'].append(agg[1])
    
    chart = QuickChart()
    chart.device_pixel_ratio = 2.0
    chart.width = 600
    chart.height = 300
    chart.config = chart_config
    chart_url = chart.get_url()

    await message.answer_photo(
      photo=chart_url,
      caption="Данные за последние 30 дней"
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
