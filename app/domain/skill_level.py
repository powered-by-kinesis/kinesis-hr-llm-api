from pydantic import BaseModel, Field
from typing import List, Optional
class Skill(BaseModel):
    skill_name: str = Field(..., description="Name of the skill being assessed")
    skill_level: str = Field(..., description="Assessed skill level (e.g., 'Beginner', 'Intermediate', 'Advanced')")
    assessment_notes: Optional[str] = Field(None, description="Additional notes or comments on the assessment")

class SkillLevelAssessmentModel(BaseModel):
    data: List[Skill] = Field(..., description="List of skills with their assessed levels and notes")