from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from BACKEND_NAME_PLACEHOLDER.model import Game, Move

WIN_CONDITIONS: list[tuple[int, int, int]] = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]


class GameService:
    def __init__(self, engine: Engine):
        self._engine: Engine = engine

    def get_board(self, game_id: int) -> list[str | None]:
        board: list[str | None] = [None] * 9
        with Session(self._engine) as session:
            stmt = (
                select(Move)
                .where(Move.game_id == game_id)
                .order_by(Move.number)
            )
            moves = list(session.scalars(stmt).all())
            for move in moves:
                symbol = "X" if move.player == self._get_player_x(session, game_id) else "O"
                board[move.position] = symbol
        return board

    def _get_player_x(self, session: Session, game_id: int) -> str:
        game = session.get(Game, game_id)
        assert game is not None
        return game.player_x

    def check_winner(self, board: list[str | None]) -> str | None:
        for a, b, c in WIN_CONDITIONS:
            if board[a] is not None and board[a] == board[b] == board[c]:
                return board[a]
        return None

    def is_draw(self, board: list[str | None]) -> bool:
        return all(cell is not None for cell in board) and self.check_winner(board) is None

    def validate_move(self, game_id: int, position: int, player: str) -> str | None:
        if position < 0 or position > 8:
            return "position must be between 0 and 8"

        with Session(self._engine) as session:
            game = session.get(Game, game_id)
            if game is None:
                return "game not found"

            if game.status != "in_progress":
                return "game is already finished"

            if player != game.player_x and player != game.player_o:
                return "player is not part of this game"

            stmt = (
                select(Move)
                .where(Move.game_id == game_id)
                .order_by(Move.number)
            )
            moves = list(session.scalars(stmt).all())

            expected_player = game.player_x if len(moves) % 2 == 0 else game.player_o
            if player != expected_player:
                return "not your turn"

            for move in moves:
                if move.position == position:
                    return "position already taken"

        return None

    def make_move(self, game_id: int, position: int, player: str) -> Move:
        with Session(self._engine) as session:
            stmt = (
                select(Move)
                .where(Move.game_id == game_id)
                .order_by(Move.number)
            )
            moves = list(session.scalars(stmt).all())
            number = len(moves) + 1

            move = Move()
            move.number = number
            move.game_id = game_id
            move.position = position
            move.player = player
            session.add(move)
            session.commit()
            session.refresh(move)

        board = self.get_board(game_id)
        winner = self.check_winner(board)

        with Session(self._engine) as session:
            game = session.get(Game, game_id)
            assert game is not None
            if winner == "X":
                game.status = "x_wins"
            elif winner == "O":
                game.status = "o_wins"
            elif self.is_draw(board):
                game.status = "draw"
            session.commit()

        return move
