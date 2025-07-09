from fastapi import APIRouter, Depends
from app.api.dependencies import get_services
from app.api.schemas import UpdateApplicationRequest  # Assuming you have a schema for the payload
from app.services import Services
from datetime import datetime

router = APIRouter(
    prefix="/webhook",
    tags=["webhook"],
    responses={404: {"description": "Not found"}},
)

@router.post("/interview-invitation")
async def update_application(payload: UpdateApplicationRequest, services: Services = Depends(get_services)):
    return {
        "applicant": services.hireai_db.applicant.update(payload.application_id, {
            "skills": payload.skills,
        }),
        "interview_invitation": services.hireai_db.interview_invitation.update(payload.invitation_interview_id, {
            "status": payload.status,
            "dateTaken": datetime.now().isoformat() if payload.status == "COMPLETED" else None,
        })
    
    }