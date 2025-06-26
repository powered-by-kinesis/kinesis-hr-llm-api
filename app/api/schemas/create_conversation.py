from pydantic import BaseModel

class ConversationRequest(BaseModel):
    query: str
    conversation_id: str
