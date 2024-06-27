from __future__ import annotations

import calendar
from datetime import datetime

def get_month_days() -> dict[str, int]:
  '''
  Returns dict with keys:
  - days_in_month: int
  - left_days_month: int
  '''
  now_year = datetime.today().year
  now_month = datetime.today().month
  now_day = datetime.today().day

  days_in_month = calendar.monthrange(
    year=now_year,
    month=now_month
  )[1]

  left_days_month = days_in_month - now_day + 1

  return {
    "days_in_month": days_in_month,
    "left_days_month": left_days_month
  }

if __name__ == "__main__":
  pass
