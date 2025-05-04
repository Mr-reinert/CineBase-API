from fastapi import APIRouter, HTTPException, Query
from services.tmdb_service import buscar_filme_por_id, buscar_em_cartaz
from utils.format import formatar_duracao, formatar_dinheiro
from datetime import datetime

router = APIRouter()

# esse aqui sobe a rota "/filmes/" aí colocando o id do lado já da pra pegar os dados desse filme
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
                "nota": f["vote_average"]
            }
            for f in dados["results"]
        ]
    }