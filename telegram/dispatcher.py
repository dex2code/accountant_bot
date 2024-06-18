from __future__ import annotations
from loguru import logger

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage


def create_telegram_dispatcher() -> Dispatcher:
  def_result = None

  try:
    def_result = Dispatcher(storage=MemoryStorage())
  
  except BaseException as E:
    logger.critical(f"Cannot create telegram Dispatcher: '{E.__repr__()}' ({E})")
    raise

  return def_result


if __name__ == "__main__":
  pass
