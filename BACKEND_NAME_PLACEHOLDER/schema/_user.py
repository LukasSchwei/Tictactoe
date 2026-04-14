from pydantic import BaseModel


class UserCreate(BaseModel):
    user_name: str
    password_hash: str


class UserFull(BaseModel):
    user_name: str
