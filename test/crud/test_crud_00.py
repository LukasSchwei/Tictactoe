from BACKEND_NAME_PLACEHOLDER.crud._user import UserCrud
from BACKEND_NAME_PLACEHOLDER.crud._game import GameCrud
from BACKEND_NAME_PLACEHOLDER.crud._move import MoveCrud
from BACKEND_NAME_PLACEHOLDER.model._base import Base
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

def setup_db():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    return Session()

def test_user_crud_create():
    db = setup_db()
    crud = UserCrud()
    user = crud.create_user(db, "player1", "hash1")
    assert user.user_name == "player1"

def test_user_crud_get():
    db = setup_db()
    crud = UserCrud()
    crud.create_user(db, "player2", "hash2")
    user = crud.get_user(db, "player2")
    assert user is not None
    assert user.user_name == "player2"

def test_user_crud_get_none():
    db = setup_db()
    crud = UserCrud()
    user = crud.get_user(db, "nonexistent")
    assert user is None

def test_user_crud_get_all():
    db = setup_db()
    crud = UserCrud()
    crud.create_user(db, "player3", "hash3")
    users = crud.get_users(db)
    assert len(users) >= 1
    assert any(u.user_name == "player3" for u in users)

def test_game_crud_create():
    db = setup_db()
    uc = UserCrud()
    gc = GameCrud()
    uc.create_user(db, "x", "1")
    uc.create_user(db, "o", "1")
    game = gc.create_game(db, "x", "o")
    assert game.id is not None
    assert game.player_x == "x"

def test_game_crud_get():
    db = setup_db()
    uc = UserCrud()
    gc = GameCrud()
    uc.create_user(db, "x", "1")
    uc.create_user(db, "o", "1")
    game = gc.create_game(db, "x", "o")
    fetched = gc.get_game(db, game.id)
    assert fetched is not None
    assert fetched.id == game.id

def test_game_crud_get_all():
    db = setup_db()
    uc = UserCrud()
    gc = GameCrud()
    uc.create_user(db, "x", "1")
    uc.create_user(db, "o", "1")
    gc.create_game(db, "x", "o")
    games = gc.get_games(db)
    assert len(games) >= 1

def test_move_crud_create():
    db = setup_db()
    uc = UserCrud()
    gc = GameCrud()
    mc = MoveCrud()
    uc.create_user(db, "x", "1")
    uc.create_user(db, "o", "1")
    game = gc.create_game(db, "x", "o")
    move = mc.create_move(db, game.id, 1, 4, "x")
    assert move.game_id == game.id
    assert move.position == 4

def test_move_crud_get():
    db = setup_db()
    uc = UserCrud()
    gc = GameCrud()
    mc = MoveCrud()
    uc.create_user(db, "x", "1")
    uc.create_user(db, "o", "1")
    game = gc.create_game(db, "x", "o")
    mc.create_move(db, game.id, 1, 4, "x")
    fetched = mc.get_move(db, game.id, 1)
    assert fetched is not None
    assert fetched.player == "x"

def test_move_crud_get_all():
    db = setup_db()
    uc = UserCrud()
    gc = GameCrud()
    mc = MoveCrud()
    uc.create_user(db, "x", "1")
    uc.create_user(db, "o", "1")
    game = gc.create_game(db, "x", "o")
    mc.create_move(db, game.id, 1, 4, "x")
    moves = mc.get_moves(db, game.id)
    assert len(moves) == 1
    assert moves[0].position == 4


