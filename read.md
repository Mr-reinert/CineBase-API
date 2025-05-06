como teste pra pegar os dados para o "em_cartaz" usei esse link
https://api.themoviedb.org/3/movie/now_playing?api_key=a5e352e95167d38103968d7ca7609755

usei isso pra evitar de criar o pycache
echo 'export PYTHONDONTWRITEBYTECODE=1' >> ~/.bashrc


se quiser subir a api no servidor use:
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload

    pra usar no terminal pra subir a api em segundo plano:
        uvicorn main:app --host 0.0.0.0 --port 8000 --reload &   




Cinebase API
Descrição
A Cinebase API é uma API RESTful construída com FastAPI para gerenciar um catálogo de filmes. Ela permite aos usuários registrar-se, fazer login, avaliar filmes e obter informações sobre os filmes.

Funcionalidades
Registro de usuário

Login de usuário com autenticação JWT

Avaliação de filmes (requer autenticação)

Obtenção de avaliações de um filme

Documentação interativa da API com Swagger

Tecnologias Utilizadas
FastAPI

Python

SQLAlchemy

PostgreSQL

Passlib

PyJWT

Pré-requisitos
Python 3.7+

PostgreSQL instalado e em execução

Poetry para gerenciamento de dependências

Instalação
Clone o repositório:

git clone <repositorio>

Navegue até o diretório do projeto:

cd Cinebase-API

Instale as dependências usando Poetry:

poetry install

Configure as variáveis de ambiente:

Crie um arquivo .env na raiz do projeto.

Defina as seguintes variáveis:

DATABASE_URL=postgresql://<usuario>:<senha>@<host>:<porta>/<nome_do_banco>
SECRET_KEY=<chave_secreta>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

Substitua os valores entre <> pelos seus valores reais.

Crie as tabelas do banco de dados:

poetry run python models/models.py

Execute a aplicação:

poetry run uvicorn main:app --reload

Uso
Documentação da API
A documentação da API pode ser acessada através do Swagger UI em /docs após a execução da aplicação.

Rotas
POST /usuarios/: Registra um novo usuário.

Campos obrigatórios: name, email, password.

POST /login/: Faz login e retorna um token JWT.

Campos obrigatórios: email, password.

GET /usuarios/me: Retorna o usuário logado (requer autenticação).

POST /filmes/{movie_id_tmdb}/avaliacoes: Cria uma avaliação para um filme (requer autenticação).

Parâmetros:

movie_id_tmdb: ID do filme no TMDB.

Campos obrigatórios: rating, comment.

GET /filmes/{movie_id_tmdb}/avaliacoes: Retorna as avaliações de um filme.

Parâmetros:

movie_id_tmdb: ID do filme no TMDB.

Autenticação
A API utiliza autenticação JWT. Para acessar rotas protegidas, é necessário enviar o token JWT no header Authorization no formato Bearer <token>.

Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.

