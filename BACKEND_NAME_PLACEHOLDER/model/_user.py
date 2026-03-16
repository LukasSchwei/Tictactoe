from typing import override

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base
from ._entity import Entity


class User(Base):
    __tablename__: str = "users"

    user_name: Mapped[str] = mapped_column(String(50), primary_key=True)
    password_hash: Mapped[str] = mapped_column(String(256), nullable=True)