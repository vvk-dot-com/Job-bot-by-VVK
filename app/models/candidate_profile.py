
from typing import Literal
from pydantic import BaseModel, Field


class SkillEvidence(BaseModel):
    name: str
    category: Literal[
        "professional",
        "project",
        "practice"
    ]
    source: str
    evidence: str


class WorkExperience(BaseModel):
    title: str
    company: str
    location: str
    duration: str


class CandidateProfile(BaseModel):
    name: str
    location: str
    overall_experience: str
    data_engineering_experience: str

    professional_summary: str

    work_experience: list[WorkExperience] = Field(
        default_factory=list
    )

    skills: list[SkillEvidence] = Field(
        default_factory=list
    )

    source_resume: str
