# 04 · Support ticket triage

**Medium · 3–5 hours to rebuild and customize** · [All projects](../../README.md)

Route an inbox to the right team with visible evidence and review flags.

[Source code](app.py) · [Sample input](sample.csv) · [Example report](../../examples/support.md) · [Claude build prompt](PROMPT.md)

## Run

From the repository root, with Python 3.11 or newer:

```bash
python run.py support
```

Reports are written to output/support.md and .json. The .prompt.md file contains the actual report and a tailored analysis request for Claude. All default demos work offline.

## Use your own input

CSV: ticket_id,subject,body. IDs must be unique. The bundled tickets are fictional. Rules are editable near the top of app.py.

```bash
python run.py support --input path/to/your-file.csv
```

## What the code does

Matches whole keywords, applies Security → Reliability → Billing → Account → Product precedence, and flags multiple/no matches. Every suggestion needs review.

## Reel demo

Show SUP-105 routed to Security with the matching words and multiple-category flag.

## Claude analysis

Review the suggested queues using the visible subjects and matching evidence. Identify ambiguous tickets and draft one clarifying question each. Do not claim the unseen full ticket is available, guarantee classification accuracy, or send replies.

Copy output/support.prompt.md into Claude, or see the [optional API setup](../../docs/USING_CLAUDE.md). The report is calculated by Python; model text is a separate draft.

## Take it further

Build a labeled evaluation set with negation and mixed-intent examples. Compare a Claude classifier with the rules before changing routing behavior.

## Sources and scope

- [Atlassian — Understanding incident severity levels](https://www.atlassian.com/incident-management/kpis/severity-levels): Real-world rationale for prioritization. The project's P1/P2/P3 keywords are original teaching rules, not Atlassian's severity taxonomy.

Review the notes in the [example report](../../examples/support.md) for assumptions and limitations.
