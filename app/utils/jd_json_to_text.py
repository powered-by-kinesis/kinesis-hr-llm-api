from app.domain import JobDescriptionModel
def job_description_to_text(jd: JobDescriptionModel) -> str:
    parts = []

    parts.append(f"Job Title: {jd.job_title}")
    
    if jd.specialization:
        parts.append("Specialization:\n- " + "\n- ".join(jd.specialization))
    if jd.seniority:
        parts.append("Seniority Level:\n- " + "\n- ".join(jd.seniority))   
    if jd.required_technical_skills:
        parts.append("Required Technical Skills:\n- " + "\n- ".join(jd.required_technical_skills))
    if jd.soft_skills_behavioral_traits:
        parts.append("Soft Skills:\n- " + "\n- ".join(jd.soft_skills_behavioral_traits))
    if jd.responsibilities:
        parts.append("Responsibilities:\n- " + "\n- ".join(jd.responsibilities))
    if jd.other_duties:
        parts.append("Other Duties:\n- " + "\n- ".join(jd.other_duties))
    if jd.preferred_background:
        parts.append("Preferred Background:\n- " + "\n- ".join(jd.preferred_background))
    if jd.domain_knowledge:
        parts.append("Domain Knowledge:\n- " + "\n- ".join(jd.domain_knowledge))
    if jd.tools_practices:
        parts.append("Tools & Practices:\n- " + "\n- ".join(jd.tools_practices))
    if jd.experience_level:
        parts.append(f"Experience Level: {jd.experience_level}")
    if jd.educational_expectation:
        parts.append(f"Educational Expectation: {jd.educational_expectation}")
    if jd.work_style:
        parts.append("Work Style:\n- " + "\n- ".join(jd.work_style))
    if jd.cultural_fit:
        parts.append("Cultural Fit:\n- " + "\n- ".join(jd.cultural_fit))
    if jd.job_type:
        parts.append(f"Job Type: {jd.job_type}")
    if jd.location:
        parts.append(f"Location: {jd.location}")
    if jd.remote_friendly is not None:
        parts.append(f"Remote Friendly: {'Yes' if jd.remote_friendly else 'No'}")

    return "\n".join(parts)
