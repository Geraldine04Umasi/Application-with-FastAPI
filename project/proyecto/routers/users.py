from fastapi import HTTPException, APIRouter
from fastapi.security import HTTPBasicCredentials
from ..database import User
from ..schemas import UserRequestModel, UserResponseModel

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
async def login(credentials: HTTPBasicCredentials):
    user = User.select().where(User.username == credentials.username).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.password != User.create_password(credentials.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return user