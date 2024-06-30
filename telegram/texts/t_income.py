from aiogram.utils.formatting import as_list, as_line, Italic


cmd_dict = {

  "info": as_list(
    as_line(
      " 💵 ⋅ Ваш указанный ежемесячный доход: ",
      Italic("{monthly_income:,}"), " ₽",
    ),
    as_line(
      " ☝ Чтобы установить новое значение,\n",
      "пришлите /income ", Italic("<значение>"), "\n",
      "Например: /income ", Italic("1200")
    )
  ).as_html(),

  "less": as_list(
    as_line(
      " 🥸 Ежемесячный доход должен быть больше цели экономии ( ",
      Italic("{monthly_goal:,}"), " ₽",
      " )",
    ),
    as_line(" ☝ Задайте правильный доход или скорректируйте цель экономии: команда /goal"),
  ).as_html(),

  "set": as_list(
    as_line(
      " 🥳 Отлично, ежемесячный доход установлен: ",
      Italic("{monthly_income:,}"), " ₽",
    ),
    as_line(" ☝ Возможно, теперь вы хотите определить ежемесячную цель? Команда /goal")
  ).as_html(),

  "wrong": as_list(
    as_line(
      " 🤔 Кажется, вы ввели значение, которое я не могу понять.\n",
      "Попробуйте еще раз, указав только цифры (целое положительное значение)"
    )
  ).as_html(),

  "error": as_list(
    as_line(" 🙀 Кажется, что-то пошло не так!"),
    as_line(" ☝ Попробуйте начать с команды /start")
  ).as_html(),

}


if __name__ == "__main__":
  pass