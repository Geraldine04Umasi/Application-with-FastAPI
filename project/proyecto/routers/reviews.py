from typing import List
from fastapi import HTTPException, APIRouter

from ..database import User, Movie, UserReview
from ..schemas import ReviewRequestModel, ReviewResponseModel, ReviewRequestPutModel

router = APIRouter(prefix='/api/v1/reviews')

@router.post('', response_model=ReviewResponseModel)
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

@router.get('', response_model=List[ReviewResponseModel])
async def get_review(page: int = 1, limit: int = 10):
    reviews = UserReview.select().paginate(page, limit) #SELECT * FROM user_reviews;
    return [user_review for user_review in reviews]

@router.get('/{review_id}')
async def get_review(review_id: int):
    user_review = UserReview.select().where(UserReview.id == review_id).first()
    if user_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    return user_review

@router.put('/{review_id}', response_model=ReviewResponseModel)
async def update_review(review_id: int, review_request: ReviewRequestPutModel):
    user_review = UserReview.select().where(UserReview.id == review_id).first()
    if user_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    
    user_review.reviews = review_request.reviews
    user_review.score = review_request.score
    user_review.save()

    return user_review


@router.delete('/reviews/{review_id}', response_model=ReviewResponseModel)
async def delete_review(review_id: int):
    user_review = UserReview.select().where(UserReview.id == review_id).first()
    if user_review is None:
        raise HTTPException(status_code=404, detail="Review not found")
    
    user_review.delete_instance()
    return {"message": "Review deleted successfully"}
