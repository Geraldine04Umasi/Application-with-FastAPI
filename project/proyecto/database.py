import os
from dotenv import load_dotenv
import hashlib
from peewee import *
from datetime import datetime

load_dotenv()

DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_HOST = os.environ.get("DB_HOST")

database = MySQLDatabase(
    DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=3306
)


class User(Model):
    username = CharField(max_length=50, unique=True)
    password = CharField(max_length=50)
    created_at = DateTimeField(default=datetime.now)

    def __str__(self):
        return self.username

    class Meta:
        database = database
        table_name = 'users'

    @classmethod
    def create_password(cls, password):
        h = hashlib.md5()
        h.update(password.encode('utf-8'))
        return h.hexdigest()

class Movie(Model):
    title = CharField(max_length=50)
    created_at = DateTimeField(default=datetime.now)

    def __str__(self):
        return self.title

    class Meta:
        database = database
        table_name = 'movies'

class UserReview(Model):
    user = ForeignKeyField(User, backref='reviews')
    movie = ForeignKeyField(Movie, backref='reviews')
    reviews = TextField()
    score = IntegerField()
    created_at = DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Review by {self.user.username} on {self.movie.title}"

    class Meta:
        database = database
        table_name = 'user_reviews'