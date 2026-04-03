from fastapi import HTTPException, APIRouter
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