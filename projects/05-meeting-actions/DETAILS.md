# 05 · Meeting action tracker

**Easy · 2–3 hours to rebuild and customize** · [All projects](../../README.md)

Turn marked meeting notes into a checklist of owners, dates and overdue tasks.

[Source code](app.py) · [Sample input](sample.md) · [Example report](../../examples/meetings.md) · [Claude build prompt](PROMPT.md)

## Run

From the repository root, with Python 3.11 or newer:

```bash
python run.py meetings --as-of 2026-09-04
```

Reports are written to output/meetings.md and .json. The .prompt.md file contains the actual report and a tailored analysis request for Claude. All default demos work offline.

## Use your own input

Markdown checkbox lines: - [ ] Owner | YYYY-MM-DD or TBD | Task. Use [x] for completed work. Use Unassigned when no owner is known. Other prose is ignored.

```bash
python run.py meetings --input path/to/your-file.md
```

## What the code does

Extracts only explicit action lines; retains source line numbers; flags overdue and missing-date tasks; reports malformed actions instead of silently treating them as completed.

## Reel demo

Show the Unassigned task with Needs date, beside Maya's overdue copy review.

## Claude analysis

Draft a meeting follow-up listing open actions grouped by owner. Cite source line numbers. Ask for clarification on Unassigned owners and TBD deadlines; never invent dates, commitments or meeting decisions.

Copy output/meetings.prompt.md into Claude, or see the [optional API setup](../../docs/USING_CLAUDE.md). The report is calculated by Python; model text is a separate draft.

## Take it further

Add an optional Claude transcript-to-action extraction step with source quotations, then require confirmation of owners and deadlines.

## Sources and scope

- [Atlassian — How to take useful meeting notes](https://www.atlassian.com/blog/teamwork/meeting-notes): Motivation for recording actionable meeting outcomes. The parser's input syntax and sample meeting are original.

Review the notes in the [example report](../../examples/meetings.md) for assumptions and limitations.
