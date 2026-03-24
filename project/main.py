from fastapi import FastAPI
from fastapi import HTTPException
from database import database as connection
from database import User, Movie, UserReview
from schemas import UserRequestModel, UserResponseModel, ReviewRequestModel, ReviewResponseModel, ReviewRequestPutModel
from typing import List
from pydantic import BaseModel

class MessageResponse(BaseModel):
    message: str

app = FastAPI(title="Proyecto para reseñar películas",
 version="1.0.0",
 description="API para reseñar películas")

@app.on_event('startup')
def startup():
    if connection.is_closed():
        connection.connect()
    
    connection.create_tables([User, Movie, UserReview])

@app.on_event('shutdown')
def shutdown():
    if not connection.is_closed():
        connection.close()
        

@app.get('/')
async def index():
    return '¡Bienvenido a la API de reseñas de películas!'

@app.post('/users', response_model=UserResponseModel)
async def create_user(user: UserRequestModel):

    if User.select().where(User.username == user.username).exists():
        raise HTTPException(status_code=409, detail="El nombre de usuario ya existe")

    hash_password = User.create_password(user.password)
    user = User.create(
        username=user.username,
        password=hash_password
    )

    return user

@app.post('/reviews', response_model=ReviewResponseModel)
async def create_reviews(user_review: ReviewRequestModel):
    if User.select().where(User.id == user_review.user_id).first() is None:
        raise HTTPException(status_code=404, detail="El usuario no existe")

    if Movie.select().where(Movie.id == user_review.movie_id).first() is None:
        raise HTTPException(status_code=404, detail="La película no existe")

    user_review = UserReview.create(
        user=user_review.user_id,
        movie=user_review.movie_id,
        reviews=user_review.reviews,
        score=user_review.score
    )

    return user_review

@app.get('/reviews/', response_model=List[ReviewResponseModel])
async def get_review():
    reviews = UserReview.select() #SELECT * FROM user_reviews;
    return [user_review for user_review in reviews]

@app.get('/reviews/{review_id}')
async def get_review(review_id: int):
    user_review = UserReview.select().where(UserReview.id == review_id).first()
    if user_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return user_review

@app.put('/reviews/{review_id}', response_model=ReviewResponseModel)
async def update_review(review_id: int, review_request: ReviewRequestPutModel):
    user_review = UserReview.select().where(UserReview.id == review_id).first()
    if user_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    
    user_review.reviews = review_request.reviews
    user_review.score = review_request.score
    user_review.save()

    return user_review


@app.delete('/reviews/{review_id}', response_model=MessageResponse)
async def delete_review(review_id: int):
    user_review = UserReview.select().where(UserReview.id == review_id).first()
    if user_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    
    user_review.delete_instance()
    return {"message": "Review deleted successfully"}
