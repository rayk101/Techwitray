"""Age unpaid invoice balances as of a chosen date."""
from datetime import date
from decimal import Decimal
from pathlib import Path

from toolkit import iso_date, money, read_csv, report, unique


def configure(parser):
    parser.add_argument("--input", type=Path, default=Path(__file__).with_name("sample.csv"))
    parser.add_argument("--as-of", type=iso_date, default=date.today())


def run(args):
    records = read_csv(args.input, ["invoice_id", "client", "due_date", "amount", "paid"])
    unique(records, "invoice_id")
    rows, total, overdue = [], Decimal(0), Decimal(0)
    for record in records:
        due = iso_date(record["due_date"])
        amount, paid = money(record["amount"]), money(record["paid"])
        if amount < 0 or paid < 0 or paid > amount:
            raise ValueError("Invoice must satisfy 0 <= paid <= amount")
        balance = amount - paid
        if balance == 0:
            continue
        days = max(0, (args.as_of - due).days)
        bucket = "Current" if days == 0 else "1-30" if days <= 30 else "31-60" if days <= 60 else "61-90" if days <= 90 else "90+"
        total += balance
        if days:
            overdue += balance
        rows.append({"Invoice": record["invoice_id"], "Client": record["client"], "Due": due.isoformat(),
                     "Days overdue": days, "Aging bucket": bucket, "Balance (USD)": f"{balance:.2f}"})
    rows.sort(key=lambda row: (-row["Days overdue"], row["Invoice"]))
    return report("Freelancer invoice tracker", {"As of": args.as_of.isoformat(), "Unpaid invoices": len(rows),
        "Outstanding (USD)": f"{total:.2f}", "Overdue (USD)": f"{overdue:.2f}"},
        ["Invoice", "Client", "Due", "Days overdue", "Aging bucket", "Balance (USD)"], rows,
        ["Fictional single-currency ledger. No reminders are sent.",
         "Paid must be the cumulative payments received AS OF the report date; payment history is not reconstructed.",
         "An invoice due today is current. This simplified report combines all balances older than 90 days."])
