"""Turn explicitly marked action items into a dated checklist."""
from datetime import date
from pathlib import Path
import re

from toolkit import iso_date, report

ACTION = re.compile(r"^\s*[-*]\s+\[([ xX])\]\s+(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*$")


def configure(parser):
    parser.add_argument("--input", type=Path, default=Path(__file__).with_name("sample.md"))
    parser.add_argument("--as-of", type=iso_date, default=date.today())


def run(args):
    rows, warnings = [], []
    for line_number, line in enumerate(args.input.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not re.match(r"^\s*[-*]\s+\[", line):
            continue
        match = ACTION.match(line)
        if not match:
            warnings.append(f"Line {line_number}: skipped malformed action; use - [ ] Owner | YYYY-MM-DD or TBD | Task")
            continue
        done, owner, due_text, task = match.groups()
        if not owner or not task:
            warnings.append(f"Line {line_number}: missing owner or task")
            continue
        due = None if due_text == "TBD" else iso_date(due_text)
        status = "Done" if done.casefold() == "x" else "Needs date" if due is None else "Overdue" if due < args.as_of else "Open"
        rows.append({"Line": line_number, "Owner": owner, "Due": due_text, "Action": task, "Status": status})
    rows.sort(key=lambda row: ({"Overdue": 0, "Needs date": 1, "Open": 2, "Done": 3}[row["Status"]], row["Due"]))
    return report("Meeting action tracker", {"As of": args.as_of.isoformat(), "Actions": len(rows),
        "Open actions": sum(row["Status"] != "Done" for row in rows), "Parsing warnings": len(warnings)},
        ["Line", "Owner", "Due", "Action", "Status"], rows,
        ["Fictional notes. Parses explicit checkbox lines only; it does not infer actions from arbitrary transcripts.",
         "TBD is kept as a missing date. An owner can be Unassigned. No calendar events or messages are created."] + warnings)
