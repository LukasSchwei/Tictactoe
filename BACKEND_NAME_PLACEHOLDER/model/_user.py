from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from ._base import Base


class User(Base):
    __tablename__: str = "users"

    user_name: Mapped[str] = mapped_column(String, primary_key=True)
    password_hash: Mapped[str] = mapped_column(String)
