from aiogram.utils.formatting import as_list, as_line, Italic


cmd_dict = {

  "today_report": as_list(
    as_line(
      " 📊 Отчет на ", Italic("{today_str}")
    ),
    as_line(
      " 🤑 За сегодняшний день потрачено: ",
      Italic("{today_spent:,}"), " ₽",
    ),
    as_line(
      " 💸 Список сегодняшних трат:",
      as_list("{today_spendings}")
    ),
    as_line(
      " 🗓 Всего за этот месяц потрачено: ",
      Italic("{this_month_spent:,}"), " ₽\n",
      "( в прошлом месяце: ",
      Italic("{last_month_spent:,}"), " ₽ )",
    ),
    as_line(
      " 🎯 Для того чтобы выполнить цель экономии ( ",
      Italic("{user_goal:,}"), " ₽ ), ",
      "Вы можете потратить еще ", Italic("{left_spends:,}"), " ₽ в этом месяце ",
      "( это примерно ", Italic("{avg_spends:,}"), " ₽ в день )",
    )
  ).as_html(),

  "error": as_list(
    as_line(f" 🙀 Кажется, что-то пошло не так!"),
    as_line(f" ☝ Попробуйте начать с команды /start")
  ).as_html(),

}


if __name__ == "__main__":
  pass