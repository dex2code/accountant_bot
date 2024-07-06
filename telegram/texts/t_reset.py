from aiogram.utils.formatting import as_list, as_line, Code

confirm_message = "Да, я уверен"

cmd_dict = {

  "confirm": as_list(
    as_line(" ⭕ Пожалуйста, подтвердите свое намерение удалить данные профиля."),
    as_line(" ‼ Будет удалена информация обо всех тратах, ежемесячном доходе и цели экономии."),
    as_line(
      " Если вы уверены, ответьте фразой: \"",
      Code(confirm_message),
      "\" или /cancel для отмены."
    )
  ).as_html(),

  "cancel": as_list(
    as_line(" 😎 Вы не подтвердили действие."),
  ).as_html(),

  "done": as_list(
    as_line(" ⭕ Данные вашего профиля удалены."),
    as_line(" ☝ Возможно, теперь вы хотите ввести новые данные? Начните с команды /income"),
  ).as_html(),

  "error": as_list(
    as_line(f" 🙀 Кажется, что-то пошло не так!"),
    as_line(f" ☝ Попробуйте начать с команды /start")
  ).as_html(),

}


if __name__ == "__main__":
  pass
