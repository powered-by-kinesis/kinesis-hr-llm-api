from llama_index.core.vector_stores.types import (
    BasePydanticVectorStore,
)
from llama_index.core.embeddings.utils import EmbedType
from llama_index.core.llms.llm import LLM
from llama_index.core import StorageContext, VectorStoreIndex

from .vector_store_index import VectorStoreIndexService
from .chat_engine import ChatEngineService
from app.services.hireai_db import HireAIDB

class Services:
    def __init__(self, vector_store: BasePydanticVectorStore, embedding_model: EmbedType, llm: LLM, hireai_db: HireAIDB):
        storage_ctx = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_vector_store(storage_context=storage_ctx, vector_store=vector_store, embed_model=embedding_model)
        self.vector_store_index_service = VectorStoreIndexService(vector_store_index=index)
        self.chat_engine_service = ChatEngineService(index=index, llm=llm, rerank_model=None)
        self.hireai_db = hireai_db
        
