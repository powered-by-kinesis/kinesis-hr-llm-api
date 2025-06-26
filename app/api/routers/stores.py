from fastapi import APIRouter, Depends, Form, File, UploadFile
from app.api.dependencies import get_services
from app.services import Services
import json

router = APIRouter(
    prefix="/stores",
    tags=["stores"],
    dependencies=[Depends(get_services)],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def store_pdf(
    metadata: str | None = Form(...),
    files: list[UploadFile] = File(...),
    services: Services = Depends(get_services),
):
    parsed_metadata = json.loads(metadata)
    services.vector_store_index_service.add(files)
    return {
        "metadata": parsed_metadata,
        "filenames": [file.filename for file in files]
    }