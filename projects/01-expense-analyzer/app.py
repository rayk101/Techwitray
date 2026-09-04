"""Summarize signed bank transactions without float rounding errors."""
from collections import defaultdict
from decimal import Decimal
from pathlib import Path
import re

from toolkit import iso_date, money, read_csv, report, unique


def configure(parser):
    parser.add_argument("--input", type=Path, default=Path(__file__).with_name("sample.csv"))
    parser.add_argument("--month", default="2026-08", help="YYYY-MM")


def run(args):
    if not re.fullmatch(r"\d{4}-\d{2}", args.month):
        raise ValueError("Month must be YYYY-MM")
    iso_date(args.month + "-01")
    rows = read_csv(args.input, ["id", "date", "description", "category", "amount"])
    unique(rows, "id")
    income, expenses = Decimal(0), Decimal(0)
    groups = defaultdict(lambda: Decimal(0))
    count = 0
    for row in rows:
        iso_date(row["date"])
        amount = money(row["amount"])
        if row["date"][:7] != args.month:
            continue
        count += 1
        if row["category"].casefold() == "income":
            income += amount
        elif row["category"].casefold() != "transfer":
            expenses -= amount
            groups[row["category"]] -= amount
    return report("Expense analyzer", {"Month": args.month, "Transactions": count,
        "Income (USD)": f"{income:.2f}", "Net spending (USD)": f"{expenses:.2f}",
        "Cash remaining (USD)": f"{income - expenses:.2f}"}, ["Category", "Net spending (USD)"],
        [{"Category": key, "Net spending (USD)": f"{value:.2f}"} for key, value in sorted(groups.items(), key=lambda item: -item[1])],
        ["Sample CSV is fictional. All amounts are USD; negative amounts are debits and positive amounts are credits.",
         "Income is an explicit category. Refunds reduce spending in their original category. Transfer rows are excluded from income and spending.",
         "This is a cash-flow summary, not tax or investment advice. Categories are supplied by the user, not inferred."])
