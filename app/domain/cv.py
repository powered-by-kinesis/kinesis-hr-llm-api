from pydantic import BaseModel, Field
from typing import List, Optional

class WorkHistoryEntry(BaseModel):
    role: str
    company: str
    duration: str
    responsibilities: List[str]

class EducationEntry(BaseModel):
    degree: str
    major: str
    institution: str

class SimpleCVModelExtract(BaseModel):
    summary: Optional[str] = Field(None, description="Summary or headline from CV")
    educations: Optional[List[EducationEntry]] = Field(None, description="List of education entries")
    experiences: Optional[List[WorkHistoryEntry]] = Field(None, description="List of work history entries")
    location: Optional[str] = Field(None, description="Location of the candidate")
    languages: Optional[List[str]] = Field(None, description="Languages spoken by the candidate")

class CVModel(BaseModel):
    full_name: Optional[str] = Field(None, description="Optional (can be ignored for matching)")
    job_title_target_role: Optional[str] = Field(None, description="If mentioned in summary or headline")
    years_of_experience: Optional[str] = Field(None, description="Total years or per-role")
    technical_skills: Optional[List[str]] = Field(None, description="e.g., ['React', 'React Native', 'TypeScript', etc.]")
    soft_skills_behavioral_traits: Optional[List[str]] = Field(None, description="e.g., ['teamwork', 'problem solving'] — if mentioned in job description")
    work_history: Optional[List[WorkHistoryEntry]] = Field(None, description="List: Role, Company, Duration, Responsibilities")
    project_experience: Optional[List[str]] = Field(None, description="Can be stored separately if mentioned")
    education: Optional[List[EducationEntry]] = Field(None, description="Degree, major, institution")
    certifications: Optional[List[str]] = Field(None, description="Relevant to technology/industry")
    industry_background: Optional[List[str]] = Field(None, description="From company (e.g., 'fintech company', 'startup', etc.)")
    tools_used: Optional[List[str]] = Field(None, description="Technical or workflow tools: Git, CI/CD, Jira, testing frameworks")
    cultural_fit_work_style: Optional[List[str]] = Field(None, description="Implicit from experience: remote, agile, startup")
    seniority: Optional[str] = Field(None, description="Estimation from years and position")
    language_communication: Optional[str] = Field(None, description="If mentioning 'led team', 'communicated with stakeholders', etc.")
