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
    player_x: Mapped[str] = mapped_column(
        ForeignKey(column=User.user_name), nullable=False
    )
    player_o: Mapped[str] = mapped_column(
        ForeignKey(column=User.user_name), nullable=False
    )

    player_x_user: Mapped[User] = relationship(foreign_keys=[player_x])
    player_o_user: Mapped[User] = relationship(foreign_keys=[player_o])
