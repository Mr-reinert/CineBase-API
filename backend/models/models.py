from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func, DECIMAL, Text, Date
from sqlalchemy.orm import relationship
from database import Base  # Importe Base do database.py
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import TIMESTAMP


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())

    reviews = relationship("Review", back_populates="user")
    watchlist_entries = relationship("Watchlist", back_populates="user")  # Alterado para watchlist_entries
    favorite_genres = relationship("Genre", secondary="user_favorite_genres", back_populates="users")
    favorite_people = relationship("Person", secondary="user_favorite_people", back_populates="users")

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    movies = relationship("Movie", secondary="movie_genres", back_populates="genres")
    users = relationship("User", secondary="user_favorite_genres", back_populates="favorite_genres")  # Alterado

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    overview = Column(Text)
    release_date = Column(Date)
    budget = Column(DECIMAL(12, 2))
    revenue = Column(DECIMAL(12, 2))
    poster_url = Column(String(255))

    genres = relationship("Genre", secondary="movie_genres", back_populates="movies")
    cast = relationship("Person", secondary="movie_cast", back_populates="movies")
    reviews = relationship("Review", back_populates="movie")
    watchlist_entries = relationship("Watchlist", back_populates="movie")

class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    role_type = Column(String(20))

    movies = relationship("Movie", secondary="movie_cast", back_populates="cast")
    performance_reviews = relationship("PerformanceReview", back_populates="person")
    users = relationship("User", secondary="user_favorite_people", back_populates="favorite_people") #Alterado

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    rating = Column(Integer)
    comment = Column(Text)
    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="reviews")
    movie = relationship("Movie", back_populates="reviews")
    tags = relationship("Tag", secondary="review_tags", back_populates="reviews")
    performance_reviews = relationship("PerformanceReview", back_populates="review")

class Watchlist(Base):
    __tablename__ = "watchlist"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), primary_key=True)
    watched = Column(Boolean, default=False)
    added_at = Column(DateTime, default=func.now())
    watched_at = Column(DateTime)

    user = relationship("User", back_populates="watchlist_entries")  # Alterado para watchlist_entries
    movie = relationship("Movie", back_populates="watchlist_entries")

class MovieGenre(Base):
    __tablename__ = "movie_genres"

    movie_id = Column(Integer, ForeignKey("movies.id"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id"), primary_key=True)

class MovieCast(Base):
    __tablename__ = "movie_cast"

    movie_id = Column(Integer, ForeignKey("movies.id"), primary_key=True)
    person_id = Column(Integer, ForeignKey("people.id"), primary_key=True)
    character_name = Column(String(100))

class UserFavoriteGenre(Base):
    __tablename__ = "user_favorite_genres"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.id"), primary_key=True)

class UserFavoritePerson(Base):
    __tablename__ = "user_favorite_people"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    person_id = Column(Integer, ForeignKey("people.id"), primary_key=True)

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(50), unique=True, nullable=False)

    reviews = relationship("Review", secondary="review_tags", back_populates="tags")

class ReviewTag(Base):
    __tablename__ = "review_tags"

    review_id = Column(Integer, ForeignKey("reviews.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)

class PerformanceReview(Base):
    __tablename__ = "performance_reviews"

    review_id = Column(Integer, ForeignKey("reviews.id"), primary_key=True)
    person_id = Column(Integer, ForeignKey("people.id"), primary_key=True)
    performance_rating = Column(Integer)

    review = relationship("Review", back_populates="performance_reviews")
    person = relationship("Person", back_populates="performance_reviews")
