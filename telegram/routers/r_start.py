from __future__ import annotations
from loguru import logger

from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import as_list, as_line, Italic

from database.classes import AccountantUser
from telegram.courier import send_text


router = Router()


@router.message(CommandStart())
@logger.catch
async def cmd_start(message: types.Message, state: FSMContext) -> None:
  logger.info(f"→ Got '{message.text}' command from {message.from_user.id}@{message.chat.id}")

  try:
    await state.clear()
    await send_text(
      message=message,
      text=as_line("Привет! 👋"),
      reply=True,
      markup=types.ReplyKeyboardRemove()
    )

    user = AccountantUser()
    user.id = message.from_user.id
    user_profile = await user.get_profile()

    if user_profile is None:
      if not await user.create_profile():
        raise Exception(f"Cannot create user profile")
      t = as_list(
        as_line(f"🧐 Я помогу вам подсчитывать ваши накопления и траты, так что вы точно будете знать состояние своего бюджета."),
        as_line("Работать со мной очень просто: в начале вы указываете свой ежемесячный доход, размер текущих накоплений и сумму, которую вы хотите откладывать каждый месяц."),
        as_line("Далее, вы начинаете регистрировать ваши траты: можно вводить каждую покупку или же раз в день присылать мне сумму потраченного."),
        as_line("После каждого вашего сообщения я буду присылать вам мини-отчет о том, как идут наши дела 📝"),
      )
      await send_text(message=message, text=t)

    t = as_list(
      as_line(f"☝ Вот как можно взаимодействовать со мной:"),
      as_line(f" 📊 ⋅ /report  → Отчет по вашему профилю"),
      as_line(f" 💵 ⋅ /income  → Ежемесячный доход"),
      as_line(f" 💰 ⋅ /savings  → Текущие накопления"),
      as_line(f" ✅ ⋅ /goal  → Ежемесячная цель"),
      as_line(f" ⭕ ⋅ /reset  → Сбросить данные профиля"),
      as_line(
        f" ✏ Чтобы записать трату, просто пришлите мне цифру в чат, например: ",
        Italic("1200"),
      )
    )
    await send_text(message=message, text=t)

  except BaseException as E:
    logger.error(E)
    t = as_list(
      as_line(f" 🙀 Кажется, что-то пошло не так!"),
      as_line(f" ☝ Попробуйте начать с команды /start")
    )
    await send_text(message=message, text=t)

  return None
