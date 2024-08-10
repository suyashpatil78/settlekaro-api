from db import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Float, DATE, JSON, ARRAY
import datetime

class ExpenseModel(db.Model):
    __tablename__ = "expenses"

    id: Mapped[str] = mapped_column(primary_key=True, unique=True)
    created_by: Mapped[str] = mapped_column(ForeignKey("users.id"))
    date: Mapped[datetime.date] = mapped_column(default=db.func.now())
    amount: Mapped[float] = mapped_column()
    expense_details: Mapped[list[JSON]] = mapped_column(ARRAY(JSON), default=[])
