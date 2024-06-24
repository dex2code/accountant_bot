from __future__ import annotations
from loguru import logger

from datetime import datetime

from sqlalchemy import select
from sqlalchemy import ForeignKey
from sqlalchemy import func as sql_func
from sqlalchemy.orm import DeclarativeBase, MappedColumn
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.dialects.sqlite import INTEGER, DATETIME

from database.engine import create_db_engine
from database.session import create_db_session


class AccountantBase(AsyncAttrs, DeclarativeBase):
  pass


class AccountantUser(AccountantBase):
  __tablename__ = "accountant_users"

  id: MappedColumn[int] = mapped_column(INTEGER, primary_key=True, nullable=False, autoincrement=True)
  monthly_income: MappedColumn[int] = mapped_column(INTEGER, nullable=False, default=0)
  savings: MappedColumn[int] = mapped_column(INTEGER, nullable=False, default=0)
  monthly_goal: MappedColumn[int] = mapped_column(INTEGER, nullable=False, default=0)
  start_dt: MappedColumn[datetime] = mapped_column(DATETIME, nullable=False, default=sql_func.current_date())

  @logger.catch
  async def get_profile(self) -> AccountantUser:
    user_profile = None

    try:
      db_engine = create_db_engine()
      db_session = create_db_session(db_engine=db_engine)
      async with db_session.begin() as db_channel:
        user_profile = await db_channel.scalar(
          statement=select(AccountantUser).where(AccountantUser.id == self.id)
        )
        await db_channel.commit()
    except BaseException as E:
      logger.error(f"Exception: {E}")
      await db_channel.rollback()
    finally:
      await db_engine.dispose()

    return user_profile


  @logger.catch
  async def create_profile(self) -> bool:
    def_result = False

    try:
      db_engine = create_db_engine()
      db_session = create_db_session(db_engine=db_engine)
      async with db_session.begin() as db_channel:
        db_channel.add(self)
        await db_channel.commit()
    except BaseException as E:
      logger.error(f"Exception: {E}")
    else:
      def_result = True
    finally:
      await db_engine.dispose()

    return def_result


  @logger.catch
  async def merge_profile(self) -> bool:
    def_result = False

    try:
      db_engine = create_db_engine()
      db_session = create_db_session(db_engine=db_engine)
      async with db_session.begin() as db_channel:
        await db_channel.merge(self)
        await db_channel.commit()
    except BaseException as E:
      logger.error(f"Exception: {E}")
      await db_channel.rollback()
    else:
      def_result = True
    finally:
      await db_engine.dispose()

    return def_result


  @logger.catch
  def __repr__(self) -> str:
    return f"AccountantUser: {self.id}, {self.monthly_income}, {self.savings}, {self.monthly_goal}, {self.start_dt}"


class AccountantOperations(AccountantBase):
  __tablename__ = "accountant_operations"

  id: MappedColumn[int] = mapped_column(INTEGER, primary_key=True, nullable=False, autoincrement=True)
  user_id: MappedColumn[int] = mapped_column(ForeignKey("accountant_users.id", ondelete="CASCADE"), index=True, nullable=False)
  operation_value: MappedColumn[int] = mapped_column(INTEGER, nullable=False, default=0)
  operation_date: MappedColumn[datetime] = mapped_column(DATETIME, index=True, nullable=False, default=sql_func.current_date())
  