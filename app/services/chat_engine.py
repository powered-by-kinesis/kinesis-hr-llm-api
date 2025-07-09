from llama_index.core import retrievers, llms, chat_engine, memory, query_engine, response_synthesizers, VectorStoreIndex, vector_stores
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.chat_engine.types import AgentChatResponse, StreamingAgentChatResponse
from typing import Optional
from pydantic import BaseModel
from typing import TypeVar
import json

T = TypeVar("T", bound=BaseModel)

class ChatEngineService:
    def __init__(self, index: VectorStoreIndex, llm: llms.LLM, rerank_model: Optional[BaseNodePostprocessor] | None):
        self.buffer_memory = memory.Memory.from_defaults(token_limit=1500)
        self.llm = llm
        self.index = index
        self.rerank_model = rerank_model

    def stream_message(self, query: str, conversation_id: str) -> StreamingAgentChatResponse:
        retriever = retrievers.VectorIndexRetriever(index=self.index, similarity_top_k=5)
        engine = chat_engine.CondensePlusContextChatEngine(
            retriever=retriever,
            llm=self.llm,
            memory=self.buffer_memory,
            node_postprocessors=[]
        )
        response = engine.stream_chat(query)
        return response

    def send_message(self, query: str, conversation_id: str) -> AgentChatResponse:
        retriever = retrievers.VectorIndexRetriever(index=self.index, similarity_top_k=5)
        engine = chat_engine.CondensePlusContextChatEngine(
            retriever=retriever,
            llm=self.llm,
            memory=self.buffer_memory,
            node_postprocessors=[]
        )
        response = engine.chat(query)
        return response
    
    async def get_structured_output(self, model_class: type[T], query: str, metadata_filters: list[dict] | None = None) -> T:
        response_synthesizer = response_synthesizers.get_response_synthesizer(
            response_mode=response_synthesizers.ResponseMode.COMPACT,
        )
        # If metadata_filters is None, we can use an empty list to avoid issues with the retriever
        filters = vector_stores.MetadataFilters.from_dicts(filter_dicts=metadata_filters) if metadata_filters else None
        retriever = retrievers.VectorIndexRetriever(index=self.index, similarity_top_k=5, filters=filters)
        engine = query_engine.RetrieverQueryEngine(
            retriever=retriever,
            response_synthesizer=response_synthesizer,
            node_postprocessors=[self.rerank_model] if self.rerank_model else []
        )
        resp = engine.query(query)

        st_llm = self.llm.as_structured_llm(model_class)
        st_text = st_llm.complete(resp.response)
        json_output = json.loads(st_text.text)

        return model_class(**json_output) if isinstance(json_output, dict) else model_class(**json.loads(json_output)) if isinstance(json_output, str) else json_output
