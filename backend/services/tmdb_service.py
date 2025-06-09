import requests
from fastapi import HTTPException
from core.config import settings


# Retorna o objeto Json que foi solicitado           
def fazer_requisicao(endpoint: str, params: dict = None):

    if params is None:
        params = {}

    headers = {"accept": "application/json"}

    # Usando Bearer Token se configurado, senão a chave de API V3
    if settings.USE_BEARER:
        headers["Authorization"] = f"Bearer {settings.BEARER_TOKEN}"
    else:
        params["api_key"] = settings.TMDB_API_KEY_V3

    try:
        resposta = requests.get(endpoint, params=params, headers=headers)
        resposta.raise_for_status()  # Lança uma exceção para status de erro (4xx ou 5xx)
        return resposta.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição para {endpoint}: {e}")
        return None  # Retorna None em caso de erro, para ser tratado por quem chama

# Função para buscar um filme específico por ID
def buscar_filme_por_id(id_filme: int) -> dict:
    endpoint = f"{settings.TMDB_URL}/movie/{id_filme}"
    params = {
        "language": "pt-BR",
        "append_to_response": "credits,watch/providers"
    }
    return fazer_requisicao(endpoint, params)



# Função para buscar filmes em cartaz
def buscar_em_cartaz(pagina: int = 1, regiao: str = "BR") -> dict:

    endpoint = f"{settings.TMDB_URL}/movie/now_playing"
    params = {
        "region": regiao,
        "page": pagina,
        "language": "pt-BR",
    }
    resposta = fazer_requisicao(endpoint, params)
    return resposta if resposta else {}



def buscar_filme_por_nome(query: str):
    url = f"{settings.TMDB_URL}/search/movie?query={query}&language=pt-BR&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {settings.BEARER_TOKEN}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro ao buscar dados no TMDB")

    dados = response.json()

    if not dados.get("results"):
        return None

    return dados["results"]  # pega o primeiro resultado da lista
