from ..crud import GameCrud, MoveCrud, UserCrud
from fastapi import FastAPI, HTTPException
from fastapi.param_functions import Depends
from ..model import Game, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

app = FastAPI(title="Tic Tac Toe API")
engine = create_engine("sqlite:///tictactoe.db")
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


game_crud = GameCrud()
move_crud = MoveCrud()
user_crud = UserCrud()


def get_board_state(db: Session, game_id: int):
    game = game_crud.get_game(db, game_id)
    if not game:
        return None
    moves = move_crud.get_moves(db, game_id)
    board = [""] * 9
    for m in moves:
        board[m.position] = "X" if m.player == game.player_x else "O"
    return game, moves, board


@app.get("/")
def get_root():
    return {"message": "Welcome to Tic Tac Toe API"}


@app.post("/user")
def create_user(username: str, password: str, db: Session = Depends(get_db)):
    user = user_crud.get_user(db, username)
    if user:
        raise HTTPException(status_code=400, detail=f"User {username} already exists")
    new_user = user_crud.create_user(db, username, password)
    return {"message": "User created", "user_name": new_user.user_name}


@app.post("/game")
def create_game(player_x: str, player_o: str, db: Session = Depends(get_db)):
    if not user_crud.get_user(db, player_x) or not user_crud.get_user(db, player_o):
        raise HTTPException(
            status_code=400, detail="Both players must be registered users first."
        )

    game = game_crud.create_game(db, player_x, player_o)
    return {
        "game_id": game.id,
        "player_x": game.player_x,
        "player_o": game.player_o,
        "status": game.status,
    }


@app.get("/game/{game_id}")
def get_game(game_id: int, db: Session = Depends(get_db)):
    state = get_board_state(db, game_id)
    if not state:
        raise HTTPException(status_code=404, detail="Game not found")

    game, moves, board = state
    current_player = game.player_x if len(moves) % 2 == 0 else game.player_o

    return {
        "game_id": game.id,
        "board": board,
        "current_player": current_player
        if not game.winner and game.status == "in_progress"
        else None,
        "winner": game.winner,
        "status": game.status,
    }


@app.post("/game/{game_id}/play/{pos}")
def play_move(game_id: int, pos: int, db: Session = Depends(get_db)):
    state = get_board_state(db, game_id)
    if not state:
        raise HTTPException(status_code=404, detail="Game not found")

    game, moves, board = state

    if game.winner or game.status != "in_progress":
        raise HTTPException(status_code=400, detail="Game is already finished.")
    if pos < 0 or pos > 8:
        raise HTTPException(status_code=400, detail="Invalid position.")
    if board[pos] != "":
        raise HTTPException(status_code=400, detail="Cell already taken.")

    current_player = game.player_x if len(moves) % 2 == 0 else game.player_o
    move_crud.create_move(db, game.id, len(moves) + 1, pos, current_player)
    board[pos] = "X" if current_player == game.player_x else "O"

    winning_combos = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]

    winner_symbol = None
    for w in winning_combos:
        if board[w[0]] and board[w[0]] == board[w[1]] == board[w[2]]:
            winner_symbol = board[w[0]]
            break

    if winner_symbol or "" not in board:
        db_game = db.get(Game, game.id)
        if winner_symbol:
            db_game.winner = game.player_x if winner_symbol == "X" else game.player_o
        else:
            db_game.winner = "Draw"
        db_game.status = "finished"
        db.commit()

        game.winner = db_game.winner
        game.status = db_game.status

    return {
        "message": "Move successful",
        "board": board,
        "winner": game.winner,
        "status": game.status,
    }
