# 🎮 Cinebase API

## Descrição

A **Cinebase API** é uma API RESTful desenvolvida com **FastAPI** para gerenciar um catálogo de filmes. Com integração ao The Movie Database (TMDB), ela permite que usuários se registrem, façam login, avaliem filmes e acessem dados atualizados de lançamentos.

---

## 🔧 Funcionalidades

* ✅ Registro de usuários
* 🔐 Autenticação com JWT (Login seguro)
* ⭐ Avaliação de filmes (autenticado)
* 🎥 Consulta a avaliações por filme
* 📄 Documentação interativa via Swagger em `/docs`
* 🔍 Busca de filmes com integração ao TMDB

---

## 🛠️ Tecnologias Utilizadas

* [FastAPI](https://fastapi.tiangolo.com/)
* [Python 3.10+](https://www.python.org/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [PostgreSQL](https://www.postgresql.org/)
* [Passlib](https://passlib.readthedocs.io/en/stable/)
* [PyJWT](https://pyjwt.readthedocs.io/)
* [Uvicorn](https://www.uvicorn.org/)

---

## 📦 Pré-requisitos

* Python 3.7 ou superior
* PostgreSQL instalado e em execução
* [Poetry](https://python-poetry.org/) para gerenciamento de dependências

---

## 🚀 Instalação

1. Clone o repositório:

   ```bash
   git clone <url-do-repositorio>
   cd cinebase-api
   ```

2. Instale as dependências com Poetry:

   ```bash
   poetry install
   ```

3. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

   ```env
   # TMDB
   USE_BEARER=true
   TMDB_API_KEY=<sua_chave_jwt>
   TMDB_API_KEY_V3=<sua_chave_v3>
   TMDB_URL=https://api.themoviedb.org/3

   # Banco de Dados
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_DB=cinebase
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/cinebase

   # JWT
   SECRET_KEY=<sua_chave_secreta>
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

4. (Opcional) Evite criar arquivos `__pycache__`:

   ```bash
   echo 'export PYTHONDONTWRITEBYTECODE=1' >> ~/.bashrc && source ~/.bashrc
   ```

5. Crie as tabelas do banco de dados:

   ```bash
   poetry run alembic upgrade head  # Ou o script que inicializa as tabelas
   ```

6. Execute a aplicação:

   ```bash
   poetry run uvicorn main:app --reload
   ```

---

## 💡 Uso

### 📘 Documentação Interativa

Acesse: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 🔐 Rotas Principais

| Método | Rota                                 | Descrição                    | Autenticação |
| ------ | ------------------------------------ | ---------------------------- | ------------ |
| POST   | `/usuarios/`                         | Registro de novo usuário     | ❌            |
| POST   | `/login/`                            | Login e geração do token JWT | ❌            |
| GET    | `/usuarios/me`                       | Dados do usuário autenticado | ✅            |
| POST   | `/filmes/{movie_id_tmdb}/avaliacoes` | Cria avaliação de um filme   | ✅            |
| GET    | `/filmes/{movie_id_tmdb}/avaliacoes` | Lista avaliações de um filme | ❌            |

---

### 🔑 Autenticação JWT

Para rotas protegidas, envie o token JWT no cabeçalho:

```http
Authorization: Bearer <seu_token>
```

---

## 🎮 Teste Rápido: Filmes em Cartaz

Para testar os filmes em cartaz diretamente da TMDB, use:

```
https://api.themoviedb.org/3/movie/now_playing?api_key=<sua_chave_v3>
```

---

## 🔢 Subindo o Servidor

Modo padrão:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Modo segundo plano (background):

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
```

---

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:

* Criar **issues**
* Sugerir **melhorias**
* Enviar **pull requests**
