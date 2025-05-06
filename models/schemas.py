from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ReviewBase(BaseModel):
    rating: int
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    user_id: int
    movie_id: int  # Este campo estará presente na resposta (avaliação existente)
    created_at: datetime

    class Config:
        from_attributes = True

class TokenData(BaseModel):
    sub: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str

class WatchlistBase(BaseModel):
    movie_id: int
    watched: bool = False

class WatchlistCreate(WatchlistBase):
    pass

class Watchlist(WatchlistBase):
    user_id: int
    added_at: datetime
    watched_at: Optional[datetime] = None

    class Config:
        from_attributes = True
