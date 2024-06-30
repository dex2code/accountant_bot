from __future__ import annotations
from loguru import logger

from datetime import datetime, date

from sqlalchemy import select, text, extract
from sqlalchemy import ForeignKey
from sqlalchemy import func as sql_func
from sqlalchemy.orm import DeclarativeBase, MappedColumn, relationship
from sqlalchemy.orm import mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.dialects.sqlite import INTEGER, DATE

from database.engine import create_db_engine
from database.session import create_db_session


class AccountantBase(AsyncAttrs, DeclarativeBase):
  pass


class AccountantUser(AccountantBase):
  __tablename__ = "accountant_users"

  id: MappedColumn[int] = mapped_column(INTEGER, primary_key=True, nullable=False, autoincrement=True)
  monthly_income: MappedColumn[int] = mapped_column(INTEGER, nullable=False, default=0)
  monthly_goal: MappedColumn[int] = mapped_column(INTEGER, nullable=False, default=0)
  start_dt: MappedColumn[date] = mapped_column(DATE, nullable=False, server_default=sql_func.current_date())
  operations = relationship("AccountantOperations", back_populates="user", cascade="all, delete, delete-orphan")

  @logger.catch
  async def get_profile(self) -> AccountantUser:
    try:
      db_engine = create_db_engine()
      db_session = create_db_session(db_engine=db_engine)
      async with db_session.begin() as db_channel:
        user_profile = await db_channel.scalar(
          statement=select(AccountantUser).where(AccountantUser.id == self.id)
        )
        await db_channel.commit()
    except BaseException as E:
      logger.error(E)
      await db_channel.rollback()
      raise
    finally:
      await db_engine.dispose()
    return user_profile

  @logger.catch
  async def create_profile(self) -> None:
    try:
      db_engine = create_db_engine()
      db_session = create_db_session(db_engine=db_engine)
      async with db_session.begin() as db_channel:
        db_channel.add(self)
        await db_channel.commit()
    except BaseException as E:
      logger.error(E)
      await db_channel.rollback()
      raise
    finally:
      await db_engine.dispose()
    return None

  @logger.catch
  async def merge_profile(self) -> None:
    try:
      db_engine = create_db_engine()
      db_session = create_db_session(db_engine=db_engine)
      async with db_session.begin() as db_channel:
        await db_channel.merge(self)
        await db_channel.commit()
    except BaseException as E:
      logger.error(E)
      await db_channel.rollback()
      raise
    finally:
      await db_engine.dispose()
    return None
  
  @logger.catch
  async def reset_profile(self) -> None:
    try:
      db_engine = create_db_engine()
      db_session = create_db_session(db_engine=db_engine)
      async with db_session.begin() as db_channel:
        await db_channel.delete(self)
        self.monthly_income = 0
        self.monthly_goal = 0
        self.start_dt = sql_func.current_date()
        db_channel.add(self)
        await db_channel.commit()
    except BaseException as E:
      logger.error(E)
      await db_channel.rollback()
      raise
    finally:
      await db_engine.dispose()
    return None


  @logger.catch
  async def get_sum_date_spendings(self, d: date) -> int:
    try:
      db_engine = create_db_engine()
      db_session = create_db_session(db_engine=db_engine)
      async with db_session.begin() as db_channel:
        sum_daily_spendings = await db_channel.scalar(
          statement=select(sql_func.sum(AccountantOperations.operation_value))
            .filter(AccountantOperations.user_id == self.id)
            .filter(AccountantOperations.operation_dt == d)
        )
        await db_channel.commit()
    except BaseException as E:
      logger.error(E)
      await db_channel.rollback()
      raise
    finally:
      await db_engine.dispose()
    return sum_daily_spendings

  @logger.catch
  async def get_sum_month_spendings(self, y: int, m: int) -> int:
    try:
      db_engine = create_db_engine()
      db_session = create_db_session(db_engine=db_engine)
      async with db_session.begin() as db_channel:
        sum_daily_spendings = await db_channel.scalar(
          statement=select(sql_func.sum(AccountantOperations.operation_value))
            .filter(AccountantOperations.user_id == self.id)
            .filter(extract('year', AccountantOperations.operation_dt) == y)
            .filter(extract('month', AccountantOperations.operation_dt) == m)
        )
        await db_channel.commit()
    except BaseException as E:
      logger.error(E)
      await db_channel.rollback()
      raise
    finally:
      await db_engine.dispose()
    return sum_daily_spendings

  @logger.catch
  async def get_sum_last_month_spendings(self) -> int:
    try:
      db_engine = create_db_engine()
      db_session = create_db_session(db_engine=db_engine)
      async with db_session.begin() as db_channel:
        sum_daily_spendings = await db_channel.scalar(
          statement=select(sql_func.sum(AccountantOperations.operation_value))
            .filter(AccountantOperations.user_id == self.id)
            .filter(extract('year', AccountantOperations.operation_dt) == datetime.today().year)
            .filter(extract('month', AccountantOperations.operation_dt) == datetime.today().month)
        )
        await db_channel.commit()
    except BaseException as E:
      logger.error(E)
      await db_channel.rollback()
      raise
    finally:
      await db_engine.dispose()
    return sum_daily_spendings


class AccountantOperations(AccountantBase):
  __tablename__ = "accountant_operations"

  id: MappedColumn[int] = mapped_column(INTEGER, primary_key=True, nullable=False, autoincrement=True)
  user_id: MappedColumn[int] = mapped_column(ForeignKey("accountant_users.id", ondelete="CASCADE"), index=True, nullable=False)
  operation_value: MappedColumn[int] = mapped_column(INTEGER, nullable=False, default=0)
  operation_dt: MappedColumn[date] = mapped_column(DATE, index=True, nullable=False, server_default=sql_func.current_date())
  user = relationship("AccountantUser", back_populates="operations")

  @logger.catch
  async def create_operation(self) -> None:
    try:
      db_engine = create_db_engine()
      db_session = create_db_session(db_engine=db_engine)
      async with db_session.begin() as db_channel:
        await db_channel.execute(
          text("PRAGMA foreign_keys=on")
        )
        db_channel.add(self)
        await db_channel.commit()
    except BaseException as E:
      logger.error(E)
      await db_channel.rollback()
      raise
    finally:
      await db_engine.dispose()
    return None
