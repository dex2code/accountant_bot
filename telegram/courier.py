from __future__ import annotations
from loguru import logger

import app_config

from aiogram.types import Message
from aiogram.utils.formatting import Text
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.types.force_reply import ForceReply


async def send_text(message: Message,
                    text: Text,
                    reply: bool=False,
                    markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None = None) -> Message:
  def_result = None

  try:
    if reply:
      def_result = await message.reply(
        text=text,
        markup=markup,
        request_timeout=app_config.telegram['timeout_sec'],
      )
    else:
      def_result = await message.answer(
        text=text,
        markup=markup,
        request_timeout=app_config.telegram['timeout_sec'],
      )

  except BaseException as E:
    logger.error(E)
    raise
  
  return def_result
