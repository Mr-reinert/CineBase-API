from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models import models, schemas  # Importa os modelos e schemas do diretório models
from core.security import verify_password, create_access_token  # Importa utilitários de segurança
from core.config import settings  # Importa configurações
from jose import JWTError, jwt

router = APIRouter(tags=["autenticação"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


# Rota para login
@router.post("/login/", response_model=schemas.Token)
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    access_token_data = {"sub": str(db_user.id)}
    access_token = create_access_token(access_token_data)
    return {"access_token": access_token, "token_type": "bearer"}


# Dependência para obter o usuário atual
async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> models.User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(sub=user_id)  # type: ignore
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.id == int(token_data.sub)).first()
    if user is None:
        raise credentials_exception
    return user
