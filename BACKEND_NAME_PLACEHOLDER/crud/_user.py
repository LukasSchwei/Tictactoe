from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from BACKEND_NAME_PLACEHOLDER.model import User


class UserCrud:
    def __init__(self, engine: Engine):
        self._engine: Engine = engine

    def get_users(self, filter: str | None = None) -> list[User]:
        with Session(self._engine) as session:
            stmt = select(User)
            if filter:
                stmt = stmt.where(User.user_name.ilike(f"%{filter}%"))
            return list(session.scalars(stmt).all())

    def get_user(self, user_name: str) -> User | None:
        with Session(self._engine) as session:
            return session.get(User, user_name)

    def create_user(
        self, user_name: str, password_hash: str, entity_id: int
    ) -> User:
        with Session(self._engine) as session:
            user = User()
            user.user_name = user_name
            user.password_hash = password_hash
            user.entity_id = entity_id
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
