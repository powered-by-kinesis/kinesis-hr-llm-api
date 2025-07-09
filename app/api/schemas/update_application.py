from pydantic import BaseModel, Field

class Skill:
    name: str
    level: str

class UpdateApplicationRequest(BaseModel):
    application_id: int
    invitation_interview_id: int
    status: str
    skills: list[dict] = Field(
        default_factory=list,
    )