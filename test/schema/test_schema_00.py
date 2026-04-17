from datetime import datetime
from BACKEND_NAME_PLACEHOLDER.schema._user import UserCreate, UserFull
from BACKEND_NAME_PLACEHOLDER.schema._game import GameCreate, GameFull
from BACKEND_NAME_PLACEHOLDER.schema._move import MoveCreate, MoveFull

def test_user_create_schema():
    user = UserCreate(user_name="test_user", password_hash="secret")
    assert user.user_name == "test_user"
    assert user.password_hash == "secret"

def test_user_create_schema_dict():
    user = UserCreate(**{"user_name": "dict", "password_hash": "pwd"})
    assert user.user_name == "dict"

def test_user_full_schema():
    user = UserFull(user_name="test_user")
    assert user.user_name == "test_user"

def test_user_full_schema_dict():
    user = UserFull(**{"user_name": "dict2"})
    assert user.user_name == "dict2"

def test_game_create_schema():
    gc = GameCreate(player_x="alice", player_o="bob")
    assert gc.player_x == "alice"
    assert gc.player_o == "bob"

def test_game_create_schema_types():
    gc = GameCreate(**{"player_x": "x", "player_o": "o"})
    assert gc.player_x == "x"

def test_game_full_schema():
    gf = GameFull(
        id=1,
        beginning_time=datetime.now(),
        status="in_progress",
        player_x="alice",
        player_o="bob",
        board=[""] * 9,
        winner=None,
    )
    assert gf.id == 1
    assert gf.status == "in_progress"

def test_game_full_schema_winner():
    gf = GameFull(
        id=2, beginning_time=datetime.now(), status="finished",
        player_x="a", player_o="b", board=["X"], winner="a"
    )
    assert gf.winner == "a"

def test_move_create_schema():
    mc = MoveCreate(position=0, player="alice")
    assert mc.position == 0
    assert mc.player == "alice"

def test_move_create_schema_dict():
    mc = MoveCreate(**{"position": 8, "player": "player"})
    assert mc.position == 8

def test_move_full_schema():
    mf = MoveFull(number=1, game_id=1, position=0, player="alice")
    assert mf.number == 1
    assert mf.game_id == 1

def test_move_full_schema_fields():
    mf = MoveFull(**{"number": 2, "game_id": 2, "position": 4, "player": "bob"})
    assert mf.player == "bob"
    assert mf.position == 4


