from routers import filmes
from fastapi import FastAPI, Depends, HTTPException,status
from sqlalchemy.orm import Session
import models, schemas
from database import engine, get_db
from passlib.context import CryptContext
from datetime import timedelta,datetime
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app = FastAPI(title="CineBase", description="API de Catálogo de Filmes")
app.include_router(filmes.router)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.get("/")
def root():
    return {"mensagem": "CineBase API está online!", "status": "OK"}





#-------------------------------------------------------------------------------------------------------------------------------



# Configuração do passlib para hashing de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(sub=user_id)
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.id == int(token_data.sub)).first()
    if user is None:
        raise credentials_exception
    return user

#----------------------------------------- ROTAS DA PARTE DE USUÁRIOS ----------------------------------------------------------
# Rota para registrar um novo usuário
@app.post("/usuarios/", response_model=schemas.User, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email já registrado")
    hashed_password = get_password_hash(user.password)
    db_user = models.User(name=user.name, email=user.email, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Rota para login de usuário
@app.post("/login/", response_model=schemas.Token)
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    access_token_data = {"sub": str(db_user.id)}
    access_token = create_access_token(access_token_data)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/usuarios/me", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

# Rota para criar uma avaliação de um filme (requer autenticação)
@app.post("/filmes/{movie_id_tmdb}/avaliacoes", response_model=schemas.Review, status_code=status.HTTP_201_CREATED)
async def create_movie_review(
    movie_id_tmdb: int,
    review: schemas.ReviewCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id_tmdb).first()
    if not db_movie:
        # Se o filme não existe no nosso banco, podemos tentar buscá-lo da TMDB
        # Por enquanto, vamos apenas levantar uma exceção
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Filme com ID TMDB {movie_id_tmdb} não encontrado")

    db_review = models.Review(
        user_id=current_user.id,
        movie_id=db_movie.id,
        rating=review.rating,
        comment=review.comment
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


# ----------------------------------- Configurações JWT-------------------------------------------------------------------------

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

SECRET_KEY = "02b767ecb8dd492ad979c7648438820cb4653fa65a33ef0bbed5b17c8c154988" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

