"""Deterministic support routing with visible rules and review flags."""
from pathlib import Path
import re

from toolkit import read_csv, report, unique

RULES = [("Security", ["breach", "data leak", "unauthorized", "account takeover"]),
         ("Reliability", ["outage", "all users", "service down"]),
         ("Billing", ["refund", "charged", "invoice", "payment"]),
         ("Account", ["login", "password", "sign in"]),
         ("Product", ["feature", "export", "dashboard"])]


def configure(parser):
    parser.add_argument("--input", type=Path, default=Path(__file__).with_name("sample.csv"))


def classify(text):
    matches = [(category, [term for term in terms if re.search(r"(?<!\w)" + re.escape(term) + r"(?!\w)", text, re.I)]) for category, terms in RULES]
    matches = [(category, terms) for category, terms in matches if terms]
    if not matches:
        return "General", "P3", "No rule matched", True
    category, terms = matches[0]
    priority = "P1" if category in ("Security", "Reliability") else "P2" if category in ("Billing", "Account") else "P3"
    return category, priority, "; ".join(f"{cat}: {', '.join(words)}" for cat, words in matches), len(matches) > 1


def run(args):
    records = read_csv(args.input, ["ticket_id", "subject", "body"])
    unique(records, "ticket_id")
    rows = []
    for record in records:
        category, priority, reasons, ambiguous = classify(record["subject"] + " " + record["body"])
        rows.append({"Ticket": record["ticket_id"], "Subject": record["subject"], "Queue": category,
                     "Priority": priority, "Evidence": reasons, "Review flag": "Multiple/no matches" if ambiguous else "Routine review"})
    rows.sort(key=lambda row: (row["Priority"], row["Ticket"]))
    return report("Support ticket triage", {"Tickets": len(rows), "P1 suggestions": sum(row["Priority"] == "P1" for row in rows)},
        ["Ticket", "Subject", "Queue", "Priority", "Evidence", "Review flag"], rows,
        ["Fictional tickets. Keywords and P1/P2/P3 rules are local teaching examples, not Atlassian severity definitions.",
         "All classifications require human review. Keyword rules miss context, negation and unfamiliar wording.",
         "Security and reliability rules take precedence over billing, account and product. No tickets are modified or messages sent."])
