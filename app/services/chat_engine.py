from llama_index.core import retrievers, llms, chat_engine, memory
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.chat_engine.types import AgentChatResponse, StreamingAgentChatResponse
from typing import Optional

class ChatEngineService:
    def __init__(self, retriever: retrievers.VectorIndexRetriever, llm: llms.LLM, rerank_model: Optional[BaseNodePostprocessor] | None):
        buffer_memory = memory.Memory.from_defaults(token_limit=1500)
        
        self.engine = chat_engine.CondensePlusContextChatEngine(
            retriever=retriever,
            llm=llm,
            memory=buffer_memory,
            node_postprocessors=[]
        )

    def stream_message(self, query: str, conversation_id: str) -> StreamingAgentChatResponse:
        response = self.engine.stream_chat(query)
        return response

    def send_message(self, query: str, conversation_id: str) -> AgentChatResponse:
        response = self.engine.chat(query)
        return response
