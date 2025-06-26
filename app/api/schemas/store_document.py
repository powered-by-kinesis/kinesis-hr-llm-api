from pydantic import BaseModel, Field
from typing import Annotated
from fastapi import File

class StoreDocumentRequest(BaseModel):
    metadata: dict = Field(
        default_factory=dict,
        description="Metadata associated with the document, such as title, author, etc."
    )
    files: Annotated[list[bytes], File()]
    