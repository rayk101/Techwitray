"""Turn public GitHub metadata into a small maintenance checklist."""
from datetime import date, datetime
from pathlib import Path
import re

from toolkit import fetch_json, iso_date, read_json, report


def configure(parser):
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--live", action="store_true")
    mode.add_argument("--input", type=Path, help="Use a GitHub repository API JSON response")
    parser.add_argument("--repo", default="psf/requests", help="Public owner/repository")
    parser.add_argument("--as-of", type=iso_date, default=date.today())


def run(args):
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", args.repo):
        raise ValueError("Repo must be owner/repository")
    if args.live:
        data = fetch_json("https://api.github.com/repos/" + args.repo,
                          {"Accept": "application/vnd.github+json"})
    else:
        if not args.input and args.repo != "psf/requests":
            raise ValueError("Different repositories require --live; the bundled snapshot is psf/requests")
        data = read_json(args.input or Path(__file__).with_name("sample.json"))
    pushed = data.get("pushed_at")
    age = (args.as_of - datetime.fromisoformat(pushed.replace("Z", "+00:00")).date()).days if pushed else None
    license_info = data.get("license") or {}
    rows = [
        {"Check": "Description", "Status": "Present" if data.get("description") else "Review", "Evidence": data.get("description") or "No description set"},
        {"Check": "Detected license", "Status": "Present" if license_info.get("spdx_id") not in (None, "NOASSERTION") else "Review", "Evidence": license_info.get("spdx_id") or "GitHub did not identify a license"},
        {"Check": "Homepage", "Status": "Present" if data.get("homepage") else "Review", "Evidence": data.get("homepage") or "No homepage set"},
        {"Check": "Archived", "Status": "Review" if data.get("archived") else "Active flag", "Evidence": str(bool(data.get("archived")))},
        {"Check": "Push recency", "Status": "Unknown" if age is None else "After report date" if age < 0 else "Review" if age > 180 else "Within 180 days", "Evidence": pushed or "No push timestamp"},
    ]
    return report("Public repository maintenance check", {"Repository": data["full_name"], "URL": data["html_url"],
        "As of": args.as_of.isoformat(), "Mode": "Live API" if args.live else "User JSON" if args.input else "Recorded API snapshot",
        "Stars": data.get("stargazers_count", "Unknown"), "Open issues + PRs": data.get("open_issues_count", "Unknown")},
        ["Check", "Status", "Evidence"], rows,
        ["Sample metadata is a real GitHub API response for psf/requests. Counts and timestamps change; see provenance.json.",
         "open_issues_count includes pull requests. A push timestamp is not necessarily a code commit on the default branch.",
         "These metadata checks do not audit security, code quality, README existence, dependency health or legal license suitability.",
         "The 180-day review threshold is a teaching heuristic. No repository settings are changed."])
