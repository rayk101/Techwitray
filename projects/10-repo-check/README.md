# 10 · Public repository maintenance check

**Medium · 3–4 hours to rebuild and customize** · [All projects](../../README.md)

Turn public repo metadata into a small, evidence-based maintenance checklist.

[Source code](app.py) · [Sample input](sample.json) · [Example report](../../examples/repocheck.md) · [Claude build prompt](PROMPT.md)

## Run

From the repository root, with Python 3.11 or newer:

```bash
python run.py repocheck --as-of 2026-09-04
```

Reports are written to output/repocheck.md and .json. The .prompt.md file contains the actual report and a tailored analysis request for Claude. All default demos work offline.

Fetch current public data:

```bash
python run.py repocheck --live --repo rayk101/Techwitray
```

The bundled JSON is a recorded snapshot, not current data. [Inspect its provenance](provenance.json).

## Use your own input

Offline: recorded psf/requests metadata. Live: public owner/repository. --input accepts another GitHub repository API JSON response. No GitHub token is required for the public endpoint.

```bash
python run.py repocheck --input path/to/your-file.json
```

## What the code does

Checks description, detected license, homepage, archived flag and push recency. Reports stars and open issues plus PRs as dated metadata, not quality scores.

## Reel demo

Run it on this public repository and point to a specific field you could improve.

## Claude analysis

Turn Review rows into a short maintenance checklist. Cite each field and avoid implying that stars or metadata prove quality, security, licensing rights or employability.

Copy output/repocheck.prompt.md into Claude, or see the [optional API setup](../../docs/USING_CLAUDE.md). The report is calculated by Python; model text is a separate draft.

## Take it further

Fetch README existence and default-branch CI status with separate API calls, then report the exact branch and commit checked.

## Sources and scope

- [GitHub — Repository REST API](https://docs.github.com/en/rest/repos/repos#get-a-repository): Public repository endpoint and returned metadata fields.
- [GitHub — REST API rate limits](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api): Public unauthenticated request limits; this project makes one request per live run.

Review the notes in the [example report](../../examples/repocheck.md) for assumptions and limitations.
