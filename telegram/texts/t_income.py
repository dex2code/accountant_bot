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
  
  "set": as_list(
    as_line(
      " 🥳 Отлично, ежемесячный доход установлен: ",
      Italic("{monthly_income:,}"), " ₽",
    ),
    as_line(" ☝ Возможно, теперь вы хотите указать размер ваших текущих накоплений? Команда /savings")
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