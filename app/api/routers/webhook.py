from fastapi import APIRouter, Depends
from app.api.dependencies import get_services
from app.api.schemas import UpdateApplicationRequest  # Assuming you have a schema for the payload
from app.services import Services
from datetime import datetime
import json

router = APIRouter(
    prefix="/webhook",
    tags=["webhook"],
    responses={404: {"description": "Not found"}},
)

@router.post("/interview-invitation")
async def update_application(payload: UpdateApplicationRequest, services: Services = Depends(get_services)):
    print(payload)
    # list to string
    try:
        transcript_str = json.dumps(payload.transcript)
        skill_levels = await services.chat_engine_service.skill_level_assessment_agent(transcript_str)
        print(f"Skill levels: {skill_levels}")
        application = services.hireai_db.applicant.update(payload.applicant_id, {
                "skills": skill_levels['data'],
            })
        return {
            "applicant": application,
            "interview_invitation": services.hireai_db.interview_invitation.update(payload.invitation_interview_id, {
                "status": payload.status,
                "dateTaken": datetime.now().isoformat() if payload.status == "COMPLETED" else None,
            })

        }
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return {"error": "Failed to process webhook"}, 500