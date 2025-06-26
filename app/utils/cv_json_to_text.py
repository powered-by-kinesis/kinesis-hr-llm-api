from app.domain import CVModel
def cv_to_text(cv: CVModel) -> str:
    parts = []

    if cv.full_name:
        parts.append(f"Full Name: {cv.full_name}")
    if cv.job_title_target_role:
        parts.append(f"Target Role: {cv.job_title_target_role}")
    if cv.years_of_experience:
        parts.append(f"Years of Experience: {cv.years_of_experience}")
    if cv.technical_skills:
        parts.append("Technical Skills:\n- " + "\n- ".join(cv.technical_skills))
    if cv.soft_skills_behavioral_traits:
        parts.append("Soft Skills:\n- " + "\n- ".join(cv.soft_skills_behavioral_traits))
    if cv.work_history:
        parts.append("Work History:")
        for job in cv.work_history:
            parts.append(f"- Role: {job.role} at {job.company} ({job.duration})")
            for r in job.responsibilities:
                parts.append(f"  • {r}")
    if cv.project_experience:
        parts.append("Project Experience:\n- " + "\n- ".join(cv.project_experience))
    if cv.education:
        parts.append("Education:")
        for edu in cv.education:
            parts.append(f"- {edu.degree} in {edu.major}, {edu.institution}")
    if cv.certifications:
        parts.append("Certifications:\n- " + "\n- ".join(cv.certifications))
    if cv.industry_background:
        parts.append("Industry Background:\n- " + "\n- ".join(cv.industry_background))
    if cv.tools_used:
        parts.append("Tools Used:\n- " + "\n- ".join(cv.tools_used))
    if cv.cultural_fit_work_style:
        parts.append("Work Style / Cultural Fit:\n- " + "\n- ".join(cv.cultural_fit_work_style))
    if cv.seniority:
        parts.append(f"Seniority: {cv.seniority}")
    if cv.language_communication:
        parts.append(f"Communication Skills: {cv.language_communication}")

    return "\n".join(parts)
