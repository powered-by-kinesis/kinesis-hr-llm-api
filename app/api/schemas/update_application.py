from pydantic import BaseModel, Field

class Skill:
    name: str
    level: str

class UpdateApplicationRequest(BaseModel):
    applicant_id: int
    invitation_interview_id: int
    status: str
    transcript: list[dict]