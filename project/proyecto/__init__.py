from fastapi import FastAPI
from .database import database as connection
from .database import User, Movie, UserReview
from typing import List
from pydantic import BaseModel
from .routers import user_router, review_router

class MessageResponse(BaseModel):
    message: str

app = FastAPI(title="Movies Review CF",
 version="1.0.0",
 description="En este proyecto se desarrolla una API para reseñas de películas utilizando FastAPI y Peewee como ORM. La API permite a los usuarios crear cuentas, agregar reseñas de películas, actualizar y eliminar reseñas existentes. Además, se implementa paginación para obtener las reseñas de manera eficiente.")

app.include_router(user_router)
app.include_router(review_router)
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



