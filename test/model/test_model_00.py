from datetime import datetime
from BACKEND_NAME_PLACEHOLDER.model._user import User
from BACKEND_NAME_PLACEHOLDER.model._game import Game
from BACKEND_NAME_PLACEHOLDER.model._move import Move
from BACKEND_NAME_PLACEHOLDER.model._base import Base

def test_user_model():
    user = User(user_name="test_user", password_hash="hash")
    assert user.user_name == "test_user"
    assert user.password_hash == "hash"
    assert user.__tablename__ == "users"

def test_user_model_attributes():
    user = User()
    user.user_name = "test"
    assert user.user_name == "test"

def test_game_model():
    game = Game(id=1, beginning_time=datetime.now(), player_x="alice", player_o="bob")
    assert game.player_x == "alice"
    assert game.player_o == "bob"
    assert game.__tablename__ == "games"

def test_game_model_status():
    game = Game(id=2)
    game.status = "finished"
    assert game.status == "finished"

def test_move_model():
    move = Move(number=1, game_id=1, position=4, player="alice")
    assert move.number == 1
    assert move.position == 4
    assert move.__tablename__ == "moves"

def test_move_model_fields():
    move = Move()
    move.number = 5
    assert move.number == 5


