from datetime import datetime

from model import Game
from sqlalchemy import select
from sqlalchemy.orm import Session


class GameCrud:
    def get_games(self, db: Session) -> list[Game]:
        stmt = select(Game)
        return list(db.scalars(stmt).all())

    def get_game(self, db: Session, game_id: int) -> Game | None:
        return db.get(Game, game_id)

    def create_game(self, db: Session, player_x: str, player_o: str) -> Game:
        game = Game()
        game.beginning_time = datetime.now()
        game.player_x = player_x
        game.player_o = player_o
        db.add(game)
        db.commit()
        db.refresh(game)
        return game
