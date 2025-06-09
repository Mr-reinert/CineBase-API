from fastapi import APIRouter, HTTPException, status, Depends, Query # Importa Depends
from sqlalchemy.orm import Session
from database import get_db
from crud import movie as movie_crud
from models import models, schemas  # Importa os modelos e schemas do diretório models
from core.auth import get_current_user # Importa get_current_user de core.auth
from services.tmdb_service import buscar_filme_por_id, buscar_em_cartaz, buscar_filme_por_nome # Importa do service
from utils.format import formatar_duracao, formatar_dinheiro, formatar_dados_tmdb # Importa do utils
from typing import List
from datetime import datetime

router = APIRouter(tags=["filmes"])

'''@router.get("/filmes/search", response_model=schemas.Movie)
def buscar_filme(query: str, db: Session = Depends(get_db)):
    # Buscar filme no banco de dados
    filme_local = movie_crud.get_movie_by_title(db, query)
    if filme_local:
        return schemas.Movie.from_orm(filme_local)

    try:
    # Se o filme não for encontrado, buscar na API externa (TMDB)
        dados_tmdb = buscar_filme_por_nome(query)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=f"Erro ao buscar filme no TMDB: {e.detail}")
    
    if not dados_tmdb:
        raise HTTPException(status_code=404, detail="Filme não encontrado no TMDB.")

    try:
        filme_formatado = formatar_dados_tmdb(dados_tmdb)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao formatar dados do TMDB: {e}")

    # Criar um novo filme com base nos dados da API
    novo_filme = schemas.MovieCreate(**filme_formatado)

    # Salvar o novo filme no banco de dados
    filme_salvo = movie_crud.create_movie(db, novo_filme)
    
    # Retornar o filme recém-criado, convertendo-o para o modelo Pydantic
    return schemas.Movie.from_orm(filme_salvo)
'''
@router.get("/filmes/search", response_model=List[schemas.Movie])
def buscar_filmes(query: str, db: Session = Depends(get_db)):
    filmes_locais = movie_crud.get_movie_by_title(db, query)  # busca parcial

    if filmes_locais:
        return [schemas.Movie.from_orm(filme) for filme in filmes_locais]

    try:
        dados_tmdb = buscar_filme_por_nome(query)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=f"Erro ao buscar filme no TMDB: {e.detail}")

    if not dados_tmdb:
        raise HTTPException(status_code=404, detail="Nenhum filme encontrado no TMDB.")

    filmes_formatados = []
    for dados_filme in dados_tmdb:
        try:
            filme_formatado = formatar_dados_tmdb(dados_filme)
            novo_filme = schemas.MovieCreate(**filme_formatado)
            filme_salvo = movie_crud.create_movie(db, novo_filme)
            filmes_formatados.append(schemas.Movie.from_orm(filme_salvo))
        except Exception as e:
            continue  # pula erros em filmes individuais

    return filmes_formatados

@router.get("/filmes/{filme_id}", tags=["Filmes"])
async def get_filme_por_id(filme_id: int, db: Session = Depends(get_db)):
    # 1. Buscar no banco de dados local
    filme_local = movie_crud.get_movie_by_tmdb_id(db, filme_id)
    if filme_local:
        return schemas.Movie.from_orm(filme_local)

    # 2. Buscar na API do TMDB se não estiver no banco
    try:
        dados = buscar_filme_por_id(filme_id)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=f"Erro ao buscar filme no TMDB: {e.detail}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro inesperado ao buscar no TMDB: {e}")

    if not dados:
        raise HTTPException(status_code=404, detail="Filme não encontrado")

    # 3. Tentar formatar os dados recebidos
    try:
        filme_formatado = formatar_dados_tmdb(dados)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao formatar dados do TMDB: {e}")

    # 4. Criar e salvar no banco
    novo_filme = schemas.MovieCreate(**filme_formatado)
    filme_salvo = movie_crud.create_movie(db, novo_filme)

    # 5. Retornar o novo filme formatado
    return schemas.Movie.from_orm(filme_salvo)


'''# esse aqui sobe a rota "/filmes/" aí colocando o id do lado já da pra pegar os dados desse filme
@router.get("/filmes/{filme_id}", tags=["Filmes"])
async def get_filme_por_id(filme_id: int):
    dados = buscar_filme_por_id(filme_id)
    if not dados:
        raise HTTPException(status_code=404, detail="Filme não encontrado")

    diretor = next((p["name"] for p in dados.get("credits", {}).get("crew", []) if p.get("job") == "Director"), "N/A")
    elenco = [
        {
            "ator": ator.get("name"),
            "personagem": ator.get("character"),
            "foto": f"https://image.tmdb.org/t/p/w200{ator.get('profile_path')}" if ator.get('profile_path') else None
        }
        for ator in dados.get("credits", {}).get("cast", [])[:5]
    ]

    return {
        "basicos": {
            "titulo": dados.get("title"),
            "sinopse": dados.get("overview", "Sinopse não disponível"),
            "poster": f"https://image.tmdb.org/t/p/w500{dados.get('poster_path')}" if dados.get('poster_path') else None,
            "ano": datetime.strptime(dados["release_date"], "%Y-%m-%d").year if dados.get("release_date") else None,
            "duracao": formatar_duracao(dados.get("runtime")),
            "classificacao": dados.get("vote_average", 0) / 2
        },
        "financeiro": {
            "orcamento": formatar_dinheiro(dados.get("budget")),
            "bilheteira": formatar_dinheiro(dados.get("revenue")),
            "lucro": formatar_dinheiro((dados.get("revenue", 0) - dados.get("budget", 0)))
        },
        "equipe": {
            "diretor": diretor,
            "elenco": elenco
        },
        "categorizacao": {
            "generos": [g["name"] for g in dados.get("genres", [])],
            "idiomas": [l["english_name"] for l in dados.get("spoken_languages", [])],
            "pais_origem": dados.get("production_countries", [{}])[0].get("name", "N/A")
        },
        "disponibilidade": {
            "streaming": [p["provider_name"] for p in dados.get("watch/providers", {}).get("results", {}).get("BR", {}).get("flatrate", [])]
        }
    }
'''
# vai mostrar os filmes que estão em cartaz
@router.get("/em_cartaz", tags=["Filmes"])
def listar_em_cartaz_formatado(regiao: str = "BR"):
    dados = buscar_em_cartaz(regiao=regiao)

    if not dados.get("results"):
        raise HTTPException(status_code=404, detail="Nada em cartaz")

    return {
        "filmes": [
            {
                "id": f["id"],
                "titulo": f["title"],
                "data": f["release_date"],
                "nota": f["vote_average"],
                "poster": f["poster_path"],
                "overview": f["overview"],
            }
            for f in dados["results"]
        ]
    }


# Rota para criar uma avaliação de um filme (requer autenticação)
@router.post("/filmes/{movie_id_tmdb}/avaliacoes", response_model=schemas.Review, status_code=status.HTTP_201_CREATED)
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

# Rota para obter as avaliações de um filme
@router.get("/filmes/{movie_id_tmdb}/avaliacoes", response_model=List[schemas.Review])
async def get_movie_reviews(
    movie_id_tmdb: int,
    db: Session = Depends(get_db)
):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id_tmdb).first()
    if not db_movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Filme com ID {movie_id_tmdb} não encontrado")

    reviews = db.query(models.Review).filter(models.Review.movie_id == db_movie.id).all()
    return reviews

@router.get("/filmes/{movie_id_tmdb}/avaliacoes", response_model=List[schemas.Review])
async def get_movie_reviews(
    movie_id_tmdb: int,
    db: Session = Depends(get_db)
):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id_tmdb).first()
    if not db_movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Filme com ID {movie_id_tmdb} não encontrado")

    reviews = db.query(models.Review).filter(models.Review.movie_id == db_movie.id).all()
    return reviews



