from aiogram.utils.formatting import as_list, as_line, Italic


cmd_dict = {

  "spent": as_list(
    as_line(
      " 💸 Новая трата: ",
      Italic("{operation_value:,}"), " ₽",
    ),
    as_line(
      " 🤑 За сегодня уже потрачено: ",
      Italic("{sum_daily_spendings:,}"), " ₽",
    )
  ).as_html(),

  "info_positive": as_list(
    as_line(
      " 🎯 Чтобы выполнить поставленную цель экономии ( ",
      Italic("{monthly_goal:,}"), " ₽",
      " ), вы можете потратить в этом месяце еще: ",
      Italic("{left_spends:,}"), " ₽\n",
      " ( Это в среднем ",
      Italic("{avg_spends:,}"), " ₽",
      " в день )"),
  ).as_html(),

  "info_negative": as_list(
    as_line(
      " 😥 В этом месяце вам не удалось выполнить поставленную цель экономии ( ",
      Italic("{monthly_goal:,}"), " ₽",
      " )",
    ),
    as_line(
      "Вы уже потратили ",
      Italic("{sum_monthly_spendings:,}"), " ₽",
      ", что на ",
      Italic("{overspent:,}"), " ₽",
      " превышает допустимые расчетные траты в этом месяце."
    ),
    as_line(
      "Осталось от ежемесячного дохода: ",
      Italic("{left_income:,}"), " ₽",
    )
  ).as_html(),

  "wrong": as_list(
    as_line(
      f" 🤔 Кажется, вы ввели значение, которое я не могу понять.\n",
      f"Попробуйте еще раз, указав только цифры (целое значение)."
    )
  ).as_html(),

  "error": as_list(
    as_line(f" 🙀 Кажется, что-то пошло не так!"),
    as_line(f" ☝ Попробуйте начать с команды /start")
  ).as_html(),

}


if __name__ == "__main__":
  pass