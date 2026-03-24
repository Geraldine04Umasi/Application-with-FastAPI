from pydantic import BaseModel, field_validator
from pydantic import ConfigDict
from typing import Any
from peewee import ModelSelect

class PeeweeGetterDict(dict):
    def __init__(self, obj):
        self._obj = obj
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, ModelSelect):
            return list(res)
        return res

class UserRequestModel(BaseModel):
    username: str
    password: str

    @field_validator('username')
    @classmethod
    def username_validator(cls, username):
        if len(username) < 3 or len(username) > 50:
            raise ValueError('El nombre de usuario debe tener entre 3 y 50 caracteres')
        return username

class ResponseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class UserResponseModel(ResponseModel):
    id: int
    username: str

class ReviewValidator(BaseModel):
    score: int

    @field_validator('score')
    @classmethod
    def score_validator(cls, score):
        if score < 1 or score > 5:
            raise ValueError('La puntuación debe estar entre 1 y 5')
        return score

class ReviewRequestModel(ReviewValidator):
    user_id: int
    movie_id: int
    reviews: str
    score: int

class ReviewResponseModel(ResponseModel):
    id: int
    movie_id: int
    reviews: str
    score: int

class ReviewRequestPutModel(ReviewValidator):
    reviews: str
    score: int