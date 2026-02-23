from typing import override

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base
from ._game import Game
from ._user import User


class Move(Base):
    __tablename__: str = "moves"

    number: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(primary_key=True)
    position: Mapped[int] = mapped_column(nullable=False)
    player: Mapped[int] = mapped_column(
        ForeignKey(column=User.user_name), nullable=False
    )

    game: Mapped[Game] = relationship()
    user: Mapped[User] = relationship()

    @override
    def __repr__(self) -> str:
        return f"User(number='{self.number}', game_id='{self.game_id}', position='{self.position}', player='{self.player}')"
