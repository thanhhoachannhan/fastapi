from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class UserRegister(BaseModel):
    email: str
    password: str
    full_name: Optional[str] = None
