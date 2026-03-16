from pydantic import BaseModel


class MoveCreate(BaseModel):
    position: int
    player: str


class MoveFull(BaseModel):
    number: int
    game_id: int
    position: int
    player: str
