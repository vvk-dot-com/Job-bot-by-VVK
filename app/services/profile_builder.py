
import re

from app.models.candidate_profile import (
    CandidateProfile,
    SkillEvidence,
    WorkExperience,
)


SKILL_RULES = [
    # Professional experience
    ("ADF Copy Activity", "project", "SELECTED DATA ENGINEERING PROJECTS"),
("ADF Data Flow", "project", "SELECTED DATA ENGINEERING PROJECTS"),
("Medallion Architecture", "project", "SELECTED DATA ENGINEERING PROJECTS"),
("Delta Lake", "project", "TECHNICAL SKILLS"),
("Parquet", "project", "SELECTED DATA ENGINEERING PROJECTS"),
("SCD Type 1", "project", "SELECTED DATA ENGINEERING PROJECTS"),
("Power BI", "project", "SELECTED DATA ENGINEERING PROJECTS"),
("Azure Key Vault", "project", "SELECTED DATA ENGINEERING PROJECTS"),
("Python", "practice", "PROFESSIONAL SUMMARY"),
]


def get_summary(text: str) -> str:
    match = re.search(
        r"PROFESSIONAL SUMMARY\s*(.*?)\s*CORE COMPETENCIES",
        text,
        re.IGNORECASE | re.DOTALL,
    )

    return match.group(1).strip() if match else ""



def extract_experience(text: str) -> list[WorkExperience]:
    pattern = re.compile(
        r"(?m)^(.+?)\s+\|\s+(.+?),\s+([^|]+?)\s+\|\s+"
        r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
        r"\s+\d{4}\s*[–-]\s*(?:Present|"
        r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
        r"\s+\d{4}))\s*$"
    )

    results = []

    for match in pattern.finditer(text):
        results.append(
            WorkExperience(
                title=match.group(1).strip(),
                company=match.group(2).strip(),
                location=match.group(3).strip(),
                duration=match.group(4).strip(),
            )
        )

    return results

SECTION_HEADINGS = [
    "PROFESSIONAL SUMMARY",
    "CORE COMPETENCIES",
    "TECHNICAL SKILLS",
    "PROFESSIONAL EXPERIENCE",
    "KEY ACHIEVEMENTS",
    "SELECTED DATA ENGINEERING PROJECTS",
    "CERTIFICATIONS & EDUCATION",
]


def get_section(text: str, heading: str) -> str:
    match = re.search(
        re.escape(heading),
        text,
        re.IGNORECASE
    )

    if not match:
        return ""

    start = match.end()
    remaining = text[start:]

    next_positions = []

    for next_heading in SECTION_HEADINGS:
        found = re.search(
            re.escape(next_heading),
            remaining,
            re.IGNORECASE
        )

        if found and found.start() > 0:
            next_positions.append(found.start())

    end = min(next_positions) if next_positions else len(remaining)

    return remaining[:end]


def extract_skills(text: str) -> list[SkillEvidence]:
    skills = []

    for name, category, source in SKILL_RULES:
        section_text = get_section(text, source)

        match = re.search(
            re.escape(name),
            section_text,
            re.IGNORECASE
        )

        if not match:
            continue

        start = max(0, match.start() - 100)
        end = min(
            len(section_text),
            match.end() + 180
        )

        evidence = " ".join(
            section_text[start:end].split()
        )

        skills.append(
            SkillEvidence(
                name=name,
                category=category,
                source=source,
                evidence=evidence,
            )
        )

    return skills

def build_candidate_profile(
    resume_text: str,
    file_name: str
) -> CandidateProfile:

    name = "VAMSHIKRISHNA VANGA"

    overall = "4 years 10 months"
    data_experience = "3 years 4 months"

    location = "Hyderabad, Telangana, India"

    return CandidateProfile(
        name=name,
        location=location,
        overall_experience=overall,
        data_engineering_experience=data_experience,
        professional_summary=get_summary(resume_text),
        work_experience=extract_experience(resume_text),
        skills=extract_skills(resume_text),
        source_resume=file_name,
    )
