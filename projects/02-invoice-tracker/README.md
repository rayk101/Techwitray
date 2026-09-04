# 02 · Freelancer invoice tracker

**Easy · 2–4 hours to rebuild and customize** · [All projects](../../README.md)

See which clients have unpaid balances and how late they are.

[Source code](app.py) · [Sample input](sample.csv) · [Example report](../../examples/invoices.md) · [Claude build prompt](PROMPT.md)

## Run

From the repository root, with Python 3.11 or newer:

```bash
python run.py invoices --as-of 2026-09-04
```

Reports are written to output/invoices.md and .json. The .prompt.md file contains the actual report and a tailored analysis request for Claude. All default demos work offline.

## Use your own input

CSV: invoice_id,client,due_date,amount,paid. USD only. paid is cumulative payments as of the chosen report date; export the ledger for that date before historical reporting.

```bash
python run.py invoices --input path/to/your-file.csv
```

## What the code does

Subtracts partial payments, excludes paid invoices, sorts oldest overdue balances first and groups by Current, 1–30, 31–60, 61–90 or 90+ days.

## Reel demo

Show INV-101 with a $1,000 balance after a $200 partial payment.

## Claude analysis

Draft a short, polite payment reminder for each overdue invoice using its exact ID, balance and due date. Do not invent fees, legal consequences or prior contact. Leave sender and payment-link placeholders. Do not send anything.

Copy output/invoices.prompt.md into Claude, or see the [optional API setup](../../docs/USING_CLAUDE.md). The report is calculated by Python; model text is a separate draft.

## Take it further

Add a separate dated payments table so historical balances can be reconstructed. Then add a reviewed reminder export.

## Sources and scope

- [Stripe — Accounts receivable aging report](https://docs.stripe.com/revenue-recognition/reports/accounts-receivable-aging): Explains outstanding balances grouped by age. Our simplified 90+ bucket combines Stripe's older ranges; this is not a Stripe integration.

Review the notes in the [example report](../../examples/invoices.md) for assumptions and limitations.
