<p align="center"><img src="assets/banner.svg" alt="Techwitray — 10 practical projects to build with Claude" width="100%"></p>

# Techwitray

**10 practical projects to build with Claude. Real code, useful outputs, easy-to-medium scope.**

[Browse all 10 projects](#the-10-projects) · [See actual output](examples/README.md) · [Use with Claude](docs/USING_CLAUDE.md) · [Sources](SOURCES.md) · [Reel script](docs/REEL.md)

[![Tests](https://github.com/rayk101/Techwitray/actions/workflows/test.yml/badge.svg)](https://github.com/rayk101/Techwitray/actions/workflows/test.yml)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/Code-MIT-27ae60)](LICENSE)

Go from an input file or public API to a result you can explain and demo. Each project has working Python code, sample input, a generated example report, a tailored Claude build prompt, documented assumptions, and links to primary sources.

The core tools calculate and validate their results locally. Claude can help you rebuild or extend them, or analyze a report through the included prompts and optional API connection. **You do not need an API key, a paid model call, or a package install to run the demos.** These are starter projects you can build with Claude; they are not a claim of Claude authorship, hiring outcomes or production readiness.

## Start in one minute

Install [Python 3.11 or newer](https://www.python.org/downloads/), then run:

```bash
git clone https://github.com/rayk101/Techwitray.git
cd Techwitray
python run.py list
python run.py demo
```

On macOS/Linux, use `python3` if `python` is unavailable. On Windows, `py` also works. You can also [download the ZIP](https://github.com/rayk101/Techwitray/archive/refs/heads/main.zip), extract it, and open a terminal in the extracted folder.

Open the generated Markdown reports in `output/`, or view the [checked-in examples](examples/README.md) directly on GitHub. Every run also saves structured JSON and a report-specific `.prompt.md` you can paste into Claude. `demo` fixes the reference date to **2026-09-04** so the sample outputs are repeatable. Individual date-based tools use today's date unless `--as-of` is supplied.

## The 10 projects

Build estimates are rough author estimates for rebuilding and customizing the scoped version after learning basic Python; they are not measured completion times. Each finished starter runs immediately.

<!-- PROJECTS_START -->
| # | Project and code | Level | Build estimate | What you get |
| --- | --- | --- | --- | --- |
| 01 | [Expense analyzer](projects/01-expense-analyzer/) | Easy | 2–3 hours | Turn a messy bank export into a monthly spending breakdown. |
| 02 | [Freelancer invoice tracker](projects/02-invoice-tracker/) | Easy | 2–4 hours | See which clients have unpaid balances and how late they are. |
| 03 | [Inventory reorder planner](projects/03-inventory-planner/) | Medium | 3–5 hours | Help a small shop spot products that need replenishment. |
| 04 | [Support ticket triage](projects/04-support-triage/) | Medium | 3–5 hours | Route an inbox to the right team with visible evidence and review flags. |
| 05 | [Meeting action tracker](projects/05-meeting-actions/) | Easy | 2–3 hours | Turn marked meeting notes into a checklist of owners, dates and overdue tasks. |
| 06 | [Campaign link builder](projects/06-campaign-links/) | Easy | 1–2 hours | Generate consistent tracking links for reels, newsletters and videos. |
| 07 | [Resume and job skill comparison](projects/07-job-match/) | Medium | 3–4 hours | Compare a resume with a job posting and show the evidence behind each match. |
| 08 | [Book discovery shortlist](projects/08-book-finder/) | Medium | 3–4 hours | Search real book metadata and export a linked reading shortlist. |
| 09 | [Outdoor filming weather planner](projects/09-weather-planner/) | Medium | 3–5 hours | Find forecast days that fit your rain and wind preferences for filming. |
| 10 | [Public repository maintenance check](projects/10-repo-check/) | Medium | 3–4 hours | Turn public repo metadata into a small, evidence-based maintenance checklist. |
<!-- PROJECTS_END -->

## Run one project

```bash
python run.py expenses --month 2026-08
python run.py invoices --as-of 2026-09-04
python run.py inventory --review-days 7
python run.py support
python run.py meetings --as-of 2026-09-04
python run.py campaigns
python run.py jobmatch
python run.py books
python run.py weather
python run.py repocheck --as-of 2026-09-04
```

Use `python run.py <project> --help` for input and output options. For example:

```bash
python run.py expenses --input my-transactions.csv --month 2026-08 --output-dir my-reports
```

## Try real, current data

Books, weather and repo checks have explicit live modes:

```bash
python run.py books --live --query "python programming" --limit 5
python run.py weather --live --latitude 40.7128 --longitude -74.0060
python run.py repocheck --live --repo rayk101/Techwitray
```

The bundled API snapshots were recorded from the named providers, with source URLs, UTC retrieval times and checksums in each project's `provenance.json`. The default weather report is a historical forecast snapshot. Business CSVs, tickets, meeting notes, campaigns and the resume are fictional examples; they are never presented as client records or scraped jobs. [Read the source register](SOURCES.md).

Open Library asks for low-volume requests and identification for regular use. GitHub's unauthenticated public API is rate limited. Open-Meteo's free hosted endpoint is for non-commercial use; review its terms before commercial deployment. Details are linked in the project guides.

## Where Claude fits

1. **Build with Claude:** Open any project's `PROMPT.md`, paste it into Claude, and work through the implementation.
2. **Analyze without an API setup:** Run the project, then paste `output/<project>.prompt.md` into Claude. Review the data before sharing it.
3. **Optional API:** Set `ANTHROPIC_API_KEY` and `ANTHROPIC_MODEL`, then add `--claude` to an individual project command. This sends the report to Anthropic and can incur API charges. See [setup and privacy details](docs/USING_CLAUDE.md).

The paid API path has mocked request/response tests. It has not been live-tested with an Anthropic key in this repository's initial verification. Local reports remain useful on their own.

## Learn, change, verify

Start with campaign links, expenses or meeting actions. Move to inventory, support triage or a live API project when you are comfortable with functions, files and validation. Each guide includes one concrete extension.

```bash
python -m unittest discover -s tests -v
```

Tests exercise business arithmetic, date boundaries, malformed input, API edge cases and the optional Claude request contract. CI runs offline on Windows and Ubuntu with Python 3.11 and 3.12. [Verification notes](docs/VERIFICATION.md).

```text
projects/       10 apps, samples, individual guides and Claude prompts
examples/       generated reports and structured JSON from the bundled samples
docs/           Claude setup, a reel script and verification notes
catalog.json    project metadata and primary references
run.py          CLI and report runner
toolkit.py      shared validation, report rendering and optional Claude API client
tests/          deterministic regression tests
tools/          explicit sample refresh and documentation generation
```

## Share it

**Repo:** [github.com/rayk101/Techwitray](https://github.com/rayk101/Techwitray)

**Reel hook:** “10 practical projects you can build with Claude — code and sources included.”

Use the [filming script](docs/REEL.md) to show inputs, working outputs and one modification. Describe only work and results you can demonstrate.

## License

[MIT](LICENSE) for original code, documentation and fictional samples. External data retains its providers' terms; see [SOURCES.md](SOURCES.md). Claude is an Anthropic product. This independent educational repository is not affiliated with or endorsed by Anthropic or the data providers.
