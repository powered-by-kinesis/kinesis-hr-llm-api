from fastapi.responses import StreamingResponse
from fastapi import APIRouter
from app.api.schemas import ConversationRequest
from llama_index.core.agent.workflow import AgentStream, ToolCallResult, ToolCall
import json
from llama_index.llms.openai import OpenAI


from sse_starlette.sse import EventSourceResponse, ServerSentEvent

from app.services.react_agent import ReActAgentService
from app.core import get_settings
import os

settings = get_settings()
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

router = APIRouter(
    prefix="/conversations",
    tags=["conversations"],
    responses={404: {"description": "Not found"}},
)

service = ReActAgentService(
    llm=OpenAI(model=settings.OPENAI_LLM_MODEL),
    connection_string=f"postgresql+psycopg2://{settings.PGUSER}:{settings.PGPASSWORD}@{settings.PGHOST}/{settings.PGDATABASE}?sslmode=require&channel_binding=require",
)

@router.post("/stream")
async def chat_stream(
    payload: ConversationRequest,
):
    handler = service.send_message(
        payload.query, payload.conversation_id
    )

    async def event_generator():
        try:
            yield ServerSentEvent(data=json.dumps({'type': 'start', 'content': '[START]'}), event="start")
            
            async for ev in handler.stream_events():
                if isinstance(ev, AgentStream):
                    yield ServerSentEvent(data=json.dumps({'type': 'message', 'content': ev.delta}), event="message")
                elif isinstance(ev, ToolCall):
                    yield ServerSentEvent(data=json.dumps({'type': 'tool_call', 'content': ev.tool_name}), event="tool_call")
            
            yield ServerSentEvent(data=json.dumps({'type': 'end', 'content': '[DONE]'}), event="end")
        finally:
            await service.save_context(payload.conversation_id, handler.ctx)


    return EventSourceResponse(
        event_generator(),
        ping=15,
    )

@router.post("/send")
async def chat_send_agent(
    payload: ConversationRequest,
):
    handler = service.send_message(
        payload.query, payload.conversation_id
    )

    response = await handler
    service.save_context(payload.conversation_id, handler.ctx)
    return {
        "data": str(response),
    }
