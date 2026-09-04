# 01 · Expense analyzer

**Easy · 2–3 hours to rebuild and customize** · [All projects](../../README.md)

Turn a messy bank export into a monthly spending breakdown.

[Source code](app.py) · [Sample input](sample.csv) · [Example report](../../examples/expenses.md) · [Claude build prompt](PROMPT.md)

## Run

From the repository root, with Python 3.11 or newer:

```bash
python run.py expenses --month 2026-08
```

Reports are written to output/expenses.md and .json. The .prompt.md file contains the actual report and a tailored analysis request for Claude. All default demos work offline.

## Use your own input

CSV: id,date,description,category,amount. Dates use YYYY-MM-DD. All amounts are USD: debits negative, credits positive. Use Income and Transfer explicitly; use spending categories for purchases and refunds.

```bash
python run.py expenses --input path/to/your-file.csv
```

## What the code does

Validates dates, unique IDs and cents; filters one month; totals income and category spending with Decimal; subtracts refunds and excludes transfers.

## Reel demo

Show Food at $148.00 after a $12.50 refund, then change the CSV and rerun.

## Claude analysis

Explain the three largest spending categories from this report. Suggest two questions the user could investigate, without prescribing spending cuts or inventing transactions.

Copy output/expenses.prompt.md into Claude, or see the [optional API setup](../../docs/USING_CLAUDE.md). The report is calculated by Python; model text is a separate draft.

## Take it further

Add editable merchant-to-category rules and a chart of monthly totals. Keep manual overrides and test refund handling.

## Sources and scope

- [CFPB — Your Money, Your Goals toolkit](https://www.consumerfinance.gov/consumer-tools/educator-tools/your-money-your-goals/toolkit/): Real-world basis for tracking and categorizing spending; sample transactions and software are original.

Review the notes in the [example report](../../examples/expenses.md) for assumptions and limitations.
