from typing import override

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ._entity import Entity


class Person(Entity):
    __tablename__: str = "persons"

    id: Mapped[int] = mapped_column(ForeignKey(column=Entity.id), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(length=255))
    last_name: Mapped[str] = mapped_column(String(length=255))

    __mapper_args__: dict[str, str] = {
        "polymorphic_identity": "persons",
    }