from typing import List
from fastapi import HTTPException, APIRouter, Response, Cookie
from fastapi.security import HTTPBasicCredentials
from ..database import User
from ..schemas import UserRequestModel, UserResponseModel, ReviewResponseModel

router = APIRouter(prefix='/api/v1/users')

@router.post('', response_model=UserResponseModel)
async def create_user(user: UserRequestModel):

    if User.select().where(User.username == user.username).exists():
        raise HTTPException(status_code=409, detail="El nombre de usuario ya existe")

    hash_password = User.create_password(user.password)
    user = User.create(
        username=user.username,
        password=hash_password
    )

    return user

@router.post('/login', response_model=UserResponseModel)
async def login(credentials: HTTPBasicCredentials, response: Response):
    user = User.select().where(User.username == credentials.username).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.password != User.create_password(credentials.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    response.set_cookie(key='user_id', value=user.id)
    
    return user

@router.get('/reviews', response_model=List[ReviewResponseModel])
async def get_reviews(user_id: int = Cookie(None)):
    user = User.select().where(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return [user_review for user_review in user.reviews]