from pydantic import BaseModel


class UserCreate(BaseModel):
    user_name: str
    password_hash: str
    entity_id: int


class UserFull(BaseModel):
    user_name: str
    entity_id: int
