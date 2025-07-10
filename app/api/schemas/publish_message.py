from pydantic import BaseModel, Field

class PublishMessageRequest(BaseModel):
    event: str = Field(
        ...,
        description="The event type that the message is associated with."
    )
    data: dict = Field(
        ...,
        description="The data payload of the message."
    )