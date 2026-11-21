
from pathlib import Path

from app.services.resume_parser import (
    extract_resume_text,
    save_extracted_text,
)

from app.services.profile_builder import (
    build_candidate_profile,
)


RESUME_PATH = "data/resumes/master_resume.pdf"

TEXT_OUTPUT = "data/resumes/master_resume_extracted.txt"

PROFILE_OUTPUT = "data/candidate_profile.json"


def main():

    print("\nAI JOB APPLICATION AGENT")
    print("=" * 40)

    print("\n[1] Reading master resume...")

    extracted = extract_resume_text(RESUME_PATH)

    print(f"Resume: {extracted['file_name']}")
    print(f"Pages: {extracted['page_count']}")

    print("\n[2] Saving extracted text...")

    save_extracted_text(
        extracted["text"],
        TEXT_OUTPUT
    )

    print("\n[3] Building candidate profile...")

    profile = build_candidate_profile(
        extracted["text"],
        extracted["file_name"]
    )

    Path(PROFILE_OUTPUT).parent.mkdir(
        parents=True,
        exist_ok=True
    )

    Path(PROFILE_OUTPUT).write_text(
        profile.model_dump_json(indent=2),
        encoding="utf-8"
    )

    print("\n[4] Candidate profile created!")

    print("\nCANDIDATE DETAILS")
    print("-" * 40)

    print(f"Name: {profile.name}")
    print(f"Location: {profile.location}")

    print(
        f"Overall experience: "
        f"{profile.overall_experience}"
    )

    print(
        f"Data Engineering experience: "
        f"{profile.data_engineering_experience}"
    )

    print("\nWORK EXPERIENCE")

    for job in profile.work_experience:
        print(
            f"- {job.title} | "
            f"{job.company} | "
            f"{job.duration}"
        )

    print("\nSKILL EVIDENCE")

    for skill in profile.skills:
        print(
            f"- {skill.name} "
            f"[{skill.category}]"
        )

    print("\nOUTPUT FILES")
    print(f"Extracted text: {TEXT_OUTPUT}")
    print(f"Candidate JSON: {PROFILE_OUTPUT}")

    print("\nResume intelligence completed!")


if __name__ == "__main__":
    main()
