from datetime import datetime
from typing import override

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ._base import Base
from ._user import User


class Game(Base):
    __tablename__: str = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    beginning_time: Mapped[datetime] = mapped_column(nullable=False)
    player_x: Mapped[int] = mapped_column(
        ForeignKey(column=User.user_name), nullable=False
    )
    player_o: Mapped[int] = mapped_column(
        ForeignKey(column=User.user_name), nullable=False
    )

    user: Mapped[User] = relationship()
