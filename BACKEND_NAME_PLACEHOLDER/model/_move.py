from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base
from ._game import Game
from ._user import User


class Move(Base):
    __tablename__: str = "moves"

    number: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey(Game.id), primary_key=True)
    position: Mapped[int] = mapped_column(nullable=False)
    player: Mapped[str] = mapped_column(ForeignKey(User.user_name), nullable=False)

    game: Mapped[Game] = relationship()
    user: Mapped[User] = relationship()
