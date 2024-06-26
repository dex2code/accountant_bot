from aiogram.utils.formatting import as_list, as_line, Italic


cmd_dict = {

  "info": as_list(
    as_line(
      " 🎯 ⋅ Ваша ежемесячная цель: ",
      Italic("{monthly_goal:,}"), " ₽",
    ),
    as_line(
      " ☝ Чтобы установить новое значение,\n",
      "пришлите /goal ", Italic("<значение>"), "\n",
      "Например: /goal ", Italic("1200")
    )
  ).as_html(),

  "set": as_list(
    as_line(
      " 🥳 Отлично, ежемесячная цель установлена: ",
      Italic("{monthly_goal:,}"), " ₽",
    ),
    as_line(" ☝ Возможно, теперь вы хотите проверить текущий статус? Команда /report")
  ).as_html(),

  "wrong": as_list(
    as_line(
      " 🤔 Кажется, вы ввели значение, которое я не могу понять.\n",
      "Попробуйте еще раз, указав только цифры (целое значение)."
    )
  ).as_html(),

  "error": as_list(
    as_line(" 🙀 Кажется, что-то пошло не так!"),
    as_line(" ☝ Попробуйте начать с команды /start")
  ).as_html(),

}


if __name__ == "__main__":
  pass