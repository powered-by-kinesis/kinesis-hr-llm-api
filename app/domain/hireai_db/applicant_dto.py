from pydantic import BaseModel, Field

class Skill(BaseModel):
    name: str
    level: str

class UpdateApplicantDTO(BaseModel):
    skills: list[Skill] = Field(default_factory=list)
    status: str = ""
