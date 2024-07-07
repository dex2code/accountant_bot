from aiogram.utils.formatting import as_list, as_line, Italic


cmd_dict = {

  "hello": as_list(
    as_line("Привет! 👋")
  ).as_html(),

  "about": as_list(
    as_line("🧐 Я помогу вам подсчитывать ваши накопления и траты так что вы точно будете знать состояние своего бюджета."),
    as_line("Работать со мной очень просто: в начале вы указываете свой средний ежемесячный доход и сумму, которую вы хотите откладывать каждый месяц."),
    as_line("Далее, вы начинаете регистрировать ваши траты: можно вводить каждую покупку или же раз в день присылать мне сумму потраченного."),
    as_line("После каждого вашего сообщения я буду присылать вам мини-отчет о том, как идут наши дела."),
  ).as_html(),

  "help": as_list(
    as_line("☝ Вот как можно взаимодействовать со мной:"),
    as_line(" 💵 ⋅ /income  →  Ежемесячный доход"),
    as_line(" 🎯 ⋅ /goal  →  Ежемесячная цель экономии"),
    as_line(" 📊 ⋅ /report  →  Отчет за месяц"),
    as_line(" 🗑 ⋅ /delete → Удалить последнюю трату"),
    as_line(" ⭕ ⋅ /reset  →  Сбросить данные профиля"),
    as_line(
      " ✏ Чтобы записать трату, просто пришлите мне цифру в чат, например: ",
      Italic("1200"),
    )
  ).as_html(),

  "clue": as_list(
    as_line("☝ Если вы новый пользователь или же только что сбросили данные своего профиля, то вам нужно указать необходимые данные. Начните с команды /income")
  ).as_html(),

  "error": as_list(
    as_line(" 🙀 Кажется, что-то пошло не так!"),
    as_line(" ☝ Попробуйте начать с команды /start")
  ).as_html(),

}


if __name__ == "__main__":
  pass