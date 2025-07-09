from fastapi import Depends
from qdrant_client import QdrantClient
from app.core import get_settings

from llama_index.vector_stores import qdrant, chroma

from llama_index.core.vector_stores.types import (
    BasePydanticVectorStore,
)
from llama_index.core.embeddings.utils import EmbedType
from llama_index.embeddings import openai, jinaai
from llama_index.core.llms import LLM
from llama_index.llms.openai import OpenAI

from app.services import Services
from app.services.hireai_db import HireAIDB

settings = get_settings()

def get_vector_stores() -> BasePydanticVectorStore: 
    # qdrant vector store
    if settings.USE_VECTOR_STORE == "qdrant":
        return qdrant.QdrantVectorStore(
            client=QdrantClient(
                host=settings.QDRANT_HOST,
                port=settings.QDRANT_PORT
            ),
            collection_name=settings.QDRANT_COLLECTION_NAME,
            enable_hybrid=True
        )

    # chroma vector store
    elif settings.USE_VECTOR_STORE == "chroma":
        return chroma.ChromaVectorStore(
            host=settings.CHROMA_HOST,
            port=settings.CHROMA_PORT,
            collection_name=settings.CHROMA_COLLECTION_NAME
        )
    else:
        raise ValueError(f"Unsupported vector store: {settings.USE_VECTOR_STORE}")

def get_llm() -> LLM:
    if settings.USE_LLM == "openai":
        return OpenAI(model=settings.OPENAI_LLM_MODEL)
    
    else:
        raise ValueError(f"Unsupported LLM: {settings.USE_LLM}")
    
def get_embedding_models() -> EmbedType:
    # OpenAI embedding model
    if settings.USE_EMBEDDING_MODEL == "openai":
        return openai.OpenAIEmbedding(
            model_name=settings.OPENAI_EMBEDDING_MODEL,
            api_key=settings.OPENAI_API_KEY
        )

    # Jina embedding model
    elif settings.USE_EMBEDDING_MODEL == "jina":
        return jinaai.JinaEmbedding(
            model=settings.JINA_EMBEDDING_MODEL,
            api_key=settings.JINA_API_KEY
        )
    else:
        raise ValueError(f"Unsupported embedding model: {settings.USE_EMBEDDING_MODEL}")
    
def get_hireai_db()-> HireAIDB:
    return HireAIDB(
        db_config={
            "dbname": settings.PGDATABASE,
            "user": settings.PGUSER,
            "password": settings.PGPASSWORD,
            "host": settings.PGHOST,
        }
    )

def get_services(
    vector_store: BasePydanticVectorStore = Depends(get_vector_stores),
    embedding_model: EmbedType = Depends(get_embedding_models),
    llm: LLM = Depends(get_llm)
) -> Services:
    return Services(
        vector_store=vector_store,
        embedding_model=embedding_model,
        llm=llm,
        hireai_db=get_hireai_db()
    )

def build_services() -> Services:
    vector_store = get_vector_stores()
    embedding_model = get_embedding_models()
    llm = get_llm()
    hireai_db = get_hireai_db()

    return Services(
        vector_store=vector_store,
        embedding_model=embedding_model,
        llm=llm,
        hireai_db=hireai_db
    )


