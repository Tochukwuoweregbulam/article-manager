from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str
    role: str = "user"


class Token(BaseModel):
    access_token: str
    token_type: str