# 07 · Resume and job skill comparison

**Medium · 3–4 hours to rebuild and customize** · [All projects](../../README.md)

Compare a resume with a job posting and show the evidence behind each match.

[Source code](app.py) · [Sample input](sample.json) · [Example report](../../examples/jobmatch.md) · [Claude build prompt](PROMPT.md)

## Run

From the repository root, with Python 3.11 or newer:

```bash
python run.py jobmatch
```

Reports are written to output/jobmatch.md and .json. The .prompt.md file contains the actual report and a tailored analysis request for Claude. All default demos work offline.

## Use your own input

JSON with resume string, job_description string and skills list. Put each resume bullet on its own line to make evidence readable. Use truthful, redacted content.

```bash
python run.py jobmatch --input path/to/your-file.json
```

## What the code does

Finds selected skill phrases in the posting, then checks exact word-bounded matches in the resume and includes the matching resume line.

## Reel demo

Show Python matched to a real resume line and Power BI missing. Call the percentage keyword coverage.

## Claude analysis

Suggest clearer wording for at most three supplied resume evidence lines, preserving the actual experience. List missing skills as questions to investigate, not qualifications to add. Do not invent metrics, credentials or hiring outcomes.

Copy output/jobmatch.prompt.md into Claude, or see the [optional API setup](../../docs/USING_CLAUDE.md). The report is calculated by Python; model text is a separate draft.

## Take it further

Add reviewed synonym groups and separate required from preferred skills. Evaluate negated phrases before adding semantic matching.

## Sources and scope

- [U.S. Department of Labor — Resume Essentials participant guide](https://www.dol.gov/sites/dolgov/files/VETS/files/ResumeEssentials_PG_Interactive_Feb2026.pdf): Supports targeted resume review and keyword/gap comparison. This tool's metric is not a validated ATS score.

Review the notes in the [example report](../../examples/jobmatch.md) for assumptions and limitations.
