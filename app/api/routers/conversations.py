from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Depends
from app.api.dependencies import get_services
from app.services import Services
from app.api.schemas import ConversationRequest

router = APIRouter(
    prefix="/conversations",
    tags=["conversations"],
    dependencies=[Depends(get_services)],
    responses={404: {"description": "Not found"}},
)

# response mode streaming
@router.post("/stream")
async def chat_stream(
    payload: ConversationRequest,
    services: Services = Depends(get_services)
):

    def event_generator():
        yield "event: start\ndata: [START]\n\n"
        for token in services.chat_engine_service.stream_message(
            payload.query, payload.conversation_id
        ).response_gen:
            yield f"event: message\ndata: {token}\n\n"
        yield "event: end\ndata: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

# response mode blocking
@router.post("/send")
async def chat_send(
    payload: ConversationRequest,
    services: Services = Depends(get_services)
):
    response = services.chat_engine_service.send_message(
        payload.query, 
        payload.conversation_id
    )
    return {
        "data": response.response
    }