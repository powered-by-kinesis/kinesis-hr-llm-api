from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # app run configurations
    APP_NAME: str = "MyApp"
    APP_VERSION: str = "1.0.0"
    USE_VECTOR_STORE: str = "qdrant"  # options: qdrant, chroma
    USE_EMBEDDING_MODEL: str = "openai"  # options: openai, jina
    USE_LLM: str = "openai"  # options: openai, jina

    #  Qdrant configurations
    QDRANT_HOST: str = ""
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION_NAME: str = ""

    # Chroma configurations
    CHROMA_HOST: str = ""
    CHROMA_PORT: int = 8008
    CHROMA_COLLECTION_NAME: str = "my_collection"

    # OpenAI configurations
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-ada-002"
    OPENAI_API_KEY: str = ""
    OPENAI_LLM_MODEL: str = "gpt-4o"  # options: gpt-3.5-turbo, gpt-4, gpt-4o

    # Jina configurations
    JINA_EMBEDDING_MODEL: str = "jina-embedding-v3"
    JINA_API_KEY: str = ""

    # llmsherpa url
    LLM_SHERPA_URL: str = ""

    PGHOST: str = ""
    PGDATABASE: str = ""
    PGUSER: str = ""
    PGPASSWORD: str = ""
    PGSSLMODE: str = ""
    PGCHANNELBINDING: str = ""

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings():
    return Settings()