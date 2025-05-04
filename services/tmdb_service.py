import os
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_URL = "https://api.themoviedb.org/3"
USE_BEARER = os.getenv("USE_BEARER", "false").lower() == "true"
API_KEY_V3 = os.getenv("TMDB_API_KEY_V3")
BEARER_TOKEN = os.getenv("TMDB_BEARER_TOKEN")

# Função utilitária para fazer as requisições, centralizando a lógica de autenticação
def fazer_requisicao(endpoint: str, params: dict = None):
    if params is None:
        params = {}

    headers = {"accept": "application/json"}
    
    # Usando Bearer Token se configurado no .env, senão a chave de API V3
    if USE_BEARER:
        headers["Authorization"] = f"Bearer {BEARER_TOKEN}"
    else:
        params["api_key"] = API_KEY_V3

    try:
        resposta = requests.get(endpoint, params=params, headers=headers)
        resposta.raise_for_status()
        return resposta.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição para {endpoint}: {e}")
        return None

# Função para buscar um filme específico por ID
def buscar_filme_por_id(id_filme: int):
    endpoint = f"{TMDB_URL}/movie/{id_filme}"
    params = {
        "language": "pt-BR",
        "append_to_response": "credits,watch/providers"
    }
    return fazer_requisicao(endpoint, params)

def buscar_em_cartaz(pagina: int = 1, regiao: str = "BR") -> dict:

    endpoint = f"{TMDB_URL}/movie/now_playing"
    params = {
        "api_key": API_KEY_V3,  # Assume que USE_BEARER = False
        "region": regiao,
        "page": pagina,
        "language": "pt-BR"
    }
    
    resposta = fazer_requisicao(endpoint, params)
    return resposta if resposta else {}

