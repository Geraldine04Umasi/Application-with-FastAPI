from pydantic import BaseModel
from pydantic import validator
from pydantic.utils import GetterDict
from typing import Any
from peewee import ModelSelect

class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)
        return res

class UserRequestModel(BaseModel):
    username: str
    password: str

    @validator('username')
    def username_validator(cls, username):
        if len(username) < 3 or len(username) > 50:
            raise ValueError('El nombre de usuario debe tener entre 3 y 50 caracteres')
        return username

class ResponseModel(BaseModel):
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict

class UserResponseModel(ResponseModel):
    id: int
    username: str

class ReviewRequestModel(BaseModel):
    user_id: int
    movie_id: int
    reviews: str
    score: int

    @validator('score')
    def score_validator(cls, score):
        if score < 1 or score > 5:
            raise ValueError('La puntuación debe estar entre 1 y 5')
        return score

class ReviewResponseModel(ResponseModel):
    id: int
    movie_id: int
    reviews: str
    score: int
