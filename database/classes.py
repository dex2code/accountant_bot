from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy import func as sql_func
from sqlalchemy.orm import DeclarativeBase, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.dialects.sqlite import INTEGER, DATE


class AccountantBase(AsyncAttrs, DeclarativeBase):
  pass


class AccountantUser(AccountantBase):
  __tablename__ = "accountant_users"

  id = mapped_column(INTEGER, primary_key=True, nullable=False, autoincrement=True)
  daily_income = mapped_column(INTEGER, nullable=False, default=0)
  initial_capital = mapped_column(INTEGER, nullable=False, default=0)
  starting_date = mapped_column(DATE, nullable=False, default=sql_func.current_date())
  operations = relationship("AccountantOperations", back_populates="user", passive_deletes=True)


class AccountantOperations(AccountantBase):
  __tablename__ = "accountant_operations"

  id = mapped_column(INTEGER, primary_key=True, nullable=False, autoincrement=True)
  user_id = mapped_column(ForeignKey("accountant_users.id", ondelete="CASCADE"), index=True, nullable=False)
  operation_date = mapped_column(DATE, index=True, nullable=False, default=sql_func.current_date())
  operation_value = mapped_column(INTEGER, nullable=False, default=0)
  user = relationship(AccountantUser, back_populates="operations")
  