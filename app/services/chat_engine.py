from llama_index.core import retrievers, llms, chat_engine, memory, query_engine, response_synthesizers, VectorStoreIndex, vector_stores, prompts
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.chat_engine.types import AgentChatResponse, StreamingAgentChatResponse
from typing import Optional
from pydantic import BaseModel
from typing import TypeVar, List
import json
from app.domain import SkillLevelAssessmentModel

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
            response_mode=response_synthesizers.ResponseMode.TREE_SUMMARIZE,
        )
        # If metadata_filters is None, we can use an empty list to avoid issues with the retriever
        filters = vector_stores.MetadataFilters.from_dicts(filter_dicts=metadata_filters) if metadata_filters else None
        retriever = retrievers.VectorIndexRetriever(index=self.index, similarity_top_k=50, sparse_top_k=52, vector_store_query_mode='hybrid', filters=filters)
        engine = query_engine.RetrieverQueryEngine(
            retriever=retriever,
            response_synthesizer=response_synthesizer,
            node_postprocessors=[self.rerank_model] if self.rerank_model else [],
        )
        retriv = retriever.retrieve(query)
        for node in retriv:
            print(f"Retrieving node: {node.get_content()}")
        resp = engine.query(query)

        print(f"Response: {resp.response}")

        st_llm = self.llm.as_structured_llm(model_class)
        st_text = st_llm.complete(resp.response)
        json_output = json.loads(st_text.text)

        return model_class(**json_output) if isinstance(json_output, dict) else model_class(**json.loads(json_output)) if isinstance(json_output, str) else json_output

    async def skill_level_assessment_agent(self, interview: str) -> dict:
        prompt = f"You are an expert in assessing skill levels based on interview transcripts. Please analyze the following interview and provide a structured assessment of the skill level for each skill mentioned. The output should be in JSON array format with the following fields: 'skill_name', 'skill_level', and 'assessment_notes' for each skill.\n\nInterview Transcript:\n{interview}"
        
        st_llm = self.llm.as_structured_llm(SkillLevelAssessmentModel)
        
        st_text = st_llm.complete(prompt)
        json_output = json.loads(st_text.text)
        
        return json_output

