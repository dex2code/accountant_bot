from aiogram.utils.formatting import as_list, as_line, Italic


cmd_dict = {

  "info": as_list(
    as_line(
      " 💵 ⋅ Ваши накопления: ",
      Italic("{savings:,}"), " ₽",
    ),
    as_line(
      " ☝ Чтобы установить новое значение,\n",
      "пришлите /savings ", Italic("<значение>"), "\n",
      "Например: /savings ", Italic("1200")
    )
  ).as_html(),

  "set": as_list(
    as_line(
      " 🥳 Отлично, размер накоплений установлен: ",
      Italic("{savings:,}"), " ₽",
    ),
    as_line(" ☝ Возможно, теперь вы хотите задать цели на месяц? Команда /goal")
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