from model import Move
from sqlalchemy import select
from sqlalchemy.orm import Session


class MoveCrud:
    def get_moves(self, db: Session, game_id: int) -> list[Move]:
        stmt = select(Move).where(Move.game_id == game_id).order_by(Move.number)
        return list(db.scalars(stmt).all())

    def get_move(self, db: Session, game_id: int, number: int) -> Move | None:
        return db.get(Move, (number, game_id))

    def create_move(
        self, db: Session, game_id: int, number: int, position: int, player: str
    ) -> Move:
        move = Move()
        move.number = number
        move.game_id = game_id
        move.position = position
        move.player = player
        db.add(move)
        db.commit()
        db.refresh(move)
        return move
