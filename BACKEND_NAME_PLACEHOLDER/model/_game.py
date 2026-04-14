from datetime import datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base
from ._user import User


class Game(Base):
    __tablename__: str = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    beginning_time: Mapped[datetime] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(String, default="in_progress")
    player_x: Mapped[str] = mapped_column(ForeignKey(User.user_name), nullable=False)
    player_o: Mapped[str] = mapped_column(ForeignKey(User.user_name), nullable=False)
    winner: Mapped[str] = mapped_column(String, nullable=True)

    player_x_user: Mapped[User] = relationship(foreign_keys=[player_x])
    player_o_user: Mapped[User] = relationship(foreign_keys=[player_o])
