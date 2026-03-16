from datetime import datetime

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from BACKEND_NAME_PLACEHOLDER.model import Game


class GameCrud:
    def __init__(self, engine: Engine):
        self._engine: Engine = engine

    def get_games(self) -> list[Game]:
        with Session(self._engine) as session:
            stmt = select(Game)
            return list(session.scalars(stmt).all())

    def get_game(self, game_id: int) -> Game | None:
        with Session(self._engine) as session:
            return session.get(Game, game_id)

    def create_game(self, player_x: str, player_o: str) -> Game:
        with Session(self._engine) as session:
            game = Game()
            game.beginning_time = datetime.now()
            game.player_x = player_x
            game.player_o = player_o
            session.add(game)
            session.commit()
            session.refresh(game)
            return game
