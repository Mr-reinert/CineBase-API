# crud/movie.py
from sqlalchemy.orm import Session
from models.models import Movie as MovieModel  # Modelo SQLAlchemy
from models.schemas import MovieCreate

def get_movie_by_title(db: Session, title: str):
    return db.query(MovieModel).filter(MovieModel.title.ilike(f"%{title}%")).all()

def get_movie_by_tmdb_id(db: Session, id: int):
    return db.query(MovieModel).filter(MovieModel.id == id).first()

def create_movie(db: Session, filme: MovieCreate):
    existente = db.query(MovieModel).filter_by(id=filme.id).first()
    if existente:
        return existente  # já existe, retorna direto
    db_movie = MovieModel(**filme.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie