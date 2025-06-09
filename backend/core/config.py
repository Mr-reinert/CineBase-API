from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str  # Padronizado para maiúsculas
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # Caso você queira usar outras variáveis do .env (MANTENHA, POIS PARECEM ÚTEIS)
    TMDB_API_KEY_V3: str
    TMDB_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    USE_BEARER: str
    BEARER_TOKEN: str

    class Config:
        env_file = ".env"
        extra = "allow"  # permite variáveis não listadas


settings = Settings()