from db import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import ARRAY, String
from sqlalchemy.sql import expression

class UserModel(db.Model):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    expenses: Mapped[list[str]] = mapped_column(ARRAY(String), default=expression.literal_column("ARRAY[]::varchar[]"))