from ..model import User
from sqlalchemy import select
from sqlalchemy.orm import Session


class UserCrud:
    def get_users(self, db: Session, filter: str | None = None) -> list[User]:
        stmt = select(User)
        if filter:
            stmt = stmt.where(User.user_name.ilike(f"%{filter}%"))
        return list(db.scalars(stmt).all())

    def get_user(self, db: Session, user_name: str) -> User | None:
        return db.get(User, user_name)

    def create_user(self, db: Session, user_name: str, password_hash: str) -> User:
        user = User()
        user.user_name = user_name
        user.password_hash = password_hash
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
