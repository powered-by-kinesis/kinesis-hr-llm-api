from pydantic import BaseModel, Field
from typing import List, Optional

class JobDescriptionModel(BaseModel):
    job_title: str = Field(..., description="e.g., 'Software Engineer - Frontend'")
    specialization: List[str] = Field(..., description="e.g., ['Frontend', 'React']")
    seniority: List[str] = Field(..., description="e.g., ['Mid', 'Senior'] — predicted from words like 'proven', 'multiple projects'")
    required_technical_skills: List[str] = Field(..., description="e.g., ['React', 'TypeScript', 'Next.js']")
    soft_skills_behavioral_traits: List[str] = Field(..., description="e.g., ['teamwork', 'communication', 'critical thinking']")
    responsibilities: List[str] = Field(..., description="Bullet points of key responsibilities")
    preferred_background: Optional[List[str]] = Field(None, description="e.g., 'startup experience', 'comfortable in fintech'")
    domain_knowledge: Optional[List[str]] = Field(None, description="e.g., 'fintech', 'ecommerce'")
    tools_practices: Optional[List[str]] = Field(None, description="e.g., ['code review', 'testing', 'agile']")
    experience_level: Optional[str] = Field(None, description="Predicted: e.g., '2+ years experience'")
    educational_expectation: Optional[str] = Field(None, description="e.g., 'Bachelor’s in Computer Science'")
    work_style: Optional[List[str]] = Field(None, description="e.g., ['cross-functional teams', 'collaborative']")
    cultural_fit: Optional[List[str]] = Field(None, description="e.g., ['fast-paced', 'startup culture']")
    job_type: Optional[str] = Field(None, description="e.g., 'Full-time', 'Contract', 'Internship'")
    location: Optional[str] = Field(None, description="e.g., 'Jakarta', 'Remote'")
    remote_friendly: Optional[bool] = Field(None, description="True if remote-friendly")
    other_duties: Optional[List[str]] = Field(None, description="Other expectations or duties if separated from responsibilities")
