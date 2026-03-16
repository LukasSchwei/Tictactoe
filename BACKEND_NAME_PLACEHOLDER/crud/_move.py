from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from BACKEND_NAME_PLACEHOLDER.model import Move


class MoveCrud:
    def __init__(self, engine: Engine):
        self._engine: Engine = engine

    def get_moves(self, game_id: int) -> list[Move]:
        with Session(self._engine) as session:
            stmt = (
                select(Move)
                .where(Move.game_id == game_id)
                .order_by(Move.number)
            )
            return list(session.scalars(stmt).all())

    def get_move(self, game_id: int, number: int) -> Move | None:
        with Session(self._engine) as session:
            return session.get(Move, (number, game_id))

    def create_move(
        self, game_id: int, number: int, position: int, player: str
    ) -> Move:
        with Session(self._engine) as session:
            move = Move()
            move.number = number
            move.game_id = game_id
            move.position = position
            move.player = player
            session.add(move)
            session.commit()
            session.refresh(move)
            return move
