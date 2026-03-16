from datetime import datetime

from pydantic import BaseModel


class GameCreate(BaseModel):
    player_x: str
    player_o: str


class GameFull(BaseModel):
    id: int
    beginning_time: datetime
    status: str
    player_x: str
    player_o: str
    board: list[str | None]
