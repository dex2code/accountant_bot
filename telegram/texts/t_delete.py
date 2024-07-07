from aiogram.utils.formatting import as_list, as_line, Italic, Code

confirm_message = "Да, я хочу удалить последнюю трату"

cmd_dict = {

  "no_spendings": as_list(
    as_line(" 🤔 У вас еще нет ни одной траты."),
    as_line(
      " ✏ Чтобы записать новую трату, просто пришлите мне цифру в чат, например: ",
      Italic("1200"),
    )
  ).as_html(),

  "confirm": as_list(
    as_line(
      " 💸 Ваша последняя трата на сумму: ",
      Italic("{last_spend_value:,}"), " ₽\n",
      "🕑 ", Italic("{last_spend_date}"),
      ", в ", Italic("{last_spend_time}")
    ),
    as_line(
      " Если вы уверены, что хотите удалить эту запись, ответьте фразой: \"",
      Code(confirm_message),
      "\" или /cancel для отмены."
    )
  ).as_html(),

  "done": as_list(
    as_line(" 🗑 Запись удалена."),
    as_line(
      " Сумма сегодняшних трат: ",
      Italic("{sum_daily_spendings}"), " ₽"
    ),
    as_line(
      " ✏ Чтобы записать новую трату, просто пришлите мне цифру в чат, например: ",
      Italic("1200"),
    )
  ).as_html(),

  "cancel": as_list(
    as_line(" 😎 Вы не подтвердили действие."),
  ).as_html(),

  "error": as_list(
    as_line(f" 🙀 Кажется, что-то пошло не так!"),
    as_line(f" ☝ Попробуйте начать с команды /start")
  ).as_html(),

}
