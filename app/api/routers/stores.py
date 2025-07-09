from fastapi import APIRouter, Depends, Form, File, UploadFile
from app.api.dependencies import get_services
from app.services import Services
from app.domain.cv import SimpleCVModelExtract
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
    await services.vector_store_index_service.add(files, metadata=parsed_metadata)
    return {
        "metadata": parsed_metadata,
        "filenames": [file.filename for file in files]
    }

@router.post("/embed-and-update-applicant")
async def embed_and_update_applicant(
    applicant_id: int = Form(...),
    files: list[UploadFile] = File(...),
    services: Services = Depends(get_services),
):
    
    await services.vector_store_index_service.add(files=files, metadata={"applicant_id": applicant_id})
    metadata_filters = [
        {"key": "applicant_id", "value": applicant_id}
    ]
    st_output = await services.chat_engine_service.get_structured_output(
        model_class=SimpleCVModelExtract,
        query="Get the summary (generate if not present), education (where he studied, such as college, elementary school, middle school, high school or vocational school), work history, location, and international languages (generate from where they live if not present)",
        metadata_filters=metadata_filters
    )

    # Update the applicant in the database with the structured output
    st_output_dict = st_output.model_dump(exclude_none=True)
    return await services.hireai_db.applicant.update(applicant_id, {
        "summary": st_output_dict['summary'] if 'summary' in st_output_dict else "",
        "education": st_output_dict['educations'] if 'educations' in st_output_dict else [],
        "experience": st_output_dict['experiences'] if 'experiences' in st_output_dict else [],
        "location": st_output_dict['location'] if 'location' in st_output_dict else [],
        "languages": st_output_dict['languages'] if 'languages' in st_output_dict else []
    })