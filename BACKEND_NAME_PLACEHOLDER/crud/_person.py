from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from BACKEND_NAME_PLACEHOLDER.model import Person


class PersonCrud:
    def __init__(self, engine: Engine):
        self._engine: Engine = engine

    def get_persons(self, filter: str | None = None) -> list[Person]:
        with Session(self._engine) as session:
            stmt = select(Person)
            if filter:
                stmt = stmt.where(
                    Person.first_name.ilike(f"%{filter}%")
                    | Person.last_name.ilike(f"%{filter}%")
                )
            return list(session.scalars(stmt).all())

    def get_person(self, person_id: int) -> Person | None:
        with Session(self._engine) as session:
            return session.get(Person, person_id)

    def create_person(
        self, name: str, first_name: str, last_name: str
    ) -> Person:
        with Session(self._engine) as session:
            person = Person()
            person.name = name
            person.first_name = first_name
            person.last_name = last_name
            session.add(person)
            session.commit()
            session.refresh(person)
            return person
