from aiogram.utils.formatting import as_list, as_line


cmd_dict = {

  "cancel": as_list(
    as_line(" ❌ Действие отменено"),
  ).as_html(),

  "error": as_list(
    as_line(" 🙀 Кажется, что-то пошло не так!"),
    as_line(" ☝ Попробуйте начать с команды /start")
  ).as_html(),

}


if __name__ == "__main__":
  pass
