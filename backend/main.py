from fastapi import FastAPI
from database import engine
from models import models  # Importa os modelos do diretório models
from routers import auth, filmes, users  # Importa os routers do diretório routers

models.Base.metadata.create_all(bind=engine)  # Cria as tabelas no banco de dados

app = FastAPI(title="CineBase", description="API de Catálogo de Filmes")

app.include_router(auth.router)    # Inclui o router de autenticação
app.include_router(filmes.router)  # Inclui o router de filmes
app.include_router(users.router)   # Inclui o router de usuários

@app.get("/")
def root():
    return {"mensagem": "CineBase API está online!", "status": "OK"}

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

