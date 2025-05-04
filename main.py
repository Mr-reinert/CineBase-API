from fastapi import FastAPI
from routers import filmes

app = FastAPI(title="CineBase", description="API de Catálogo de Filmes")
app.include_router(filmes.router)

@app.get("/")
def root():
    return {"mensagem": "CineBase API está online!", "status": "OK"}