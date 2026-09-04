"""Explain explicit skill overlap without inventing qualifications."""
from pathlib import Path
import re

from toolkit import read_json, report


def configure(parser):
    parser.add_argument("--input", type=Path, default=Path(__file__).with_name("sample.json"))


def contains(text, phrase):
    return re.search(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", text, re.I) is not None


def run(args):
    data = read_json(args.input)
    resume, job, skills = data["resume"], data["job_description"], data["skills"]
    if not isinstance(resume, str) or not isinstance(job, str) or not isinstance(skills, list):
        raise ValueError("Expected resume and job_description strings, and a skills list")
    if not resume.strip() or not job.strip() or any(not isinstance(skill, str) or not skill.strip() for skill in skills):
        raise ValueError("Resume, job description, and skill names must not be blank")
    skills = list(dict.fromkeys(skill.strip().lower() for skill in skills))
    rows = []
    for skill in skills:
        if not contains(job, skill):
            continue
        evidence = next((line.strip() for line in resume.splitlines() if contains(line, skill)), "Not found in supplied resume")
        rows.append({"Skill": skill, "Resume evidence": evidence, "Match": "Present" if contains(resume, skill) else "Missing"})
    matched = sum(row["Match"] == "Present" for row in rows)
    return report("Resume and job skill comparison", {"Skills identified in posting": len(rows), "Skills mentioned in resume": matched,
        "Keyword coverage": f"{matched / len(rows):.0%}" if rows else "N/A — no selected skills found"},
        ["Skill", "Resume evidence", "Match"], rows,
        ["Fictional resume and job posting. Skill vocabulary is user supplied; exact phrases use word boundaries.",
         "Keyword coverage is not an ATS score, employability prediction or proof of proficiency. Negation, synonyms and experience level are not interpreted.",
         "Use missing skills as review prompts. Add experience to a resume only when it is true."])
