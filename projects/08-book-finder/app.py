"""Find real books through Open Library's search API."""
import os
from pathlib import Path
from urllib.parse import urlencode

from toolkit import USER_AGENT, fetch_json, read_json, report

ENDPOINT = "https://openlibrary.org/search.json"


def configure(parser):
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--live", action="store_true", help="Search Open Library over the network")
    mode.add_argument("--input", type=Path, help="Use an Open Library JSON response")
    parser.add_argument("--query", default="python programming")
    parser.add_argument("--limit", type=int, default=5)


def run(args):
    if not 1 <= args.limit <= 20 or not args.query.strip():
        raise ValueError("Use a nonblank query and limit between 1 and 20")
    url = ENDPOINT + "?" + urlencode({"q": args.query, "limit": args.limit, "fields": "key,title,author_name,first_publish_year,edition_count"})
    if args.live:
        contact = os.getenv("OPENLIBRARY_CONTACT", "").strip()
        headers = {"User-Agent": USER_AGENT + (f" ({contact})" if contact else "")}
        data = fetch_json(url, headers)
    else:
        if not args.input and args.query != "python programming":
            raise ValueError("Changing the query requires --live; the bundled snapshot is for python programming")
        data = read_json(args.input or Path(__file__).with_name("sample.json"))
    rows = []
    for book in data.get("docs", [])[:args.limit]:
        key = book.get("key", "")
        rows.append({"Title": book.get("title") or "Unknown title", "Authors": ", ".join(book.get("author_name") or []) or "Unknown",
                     "First publication": book.get("first_publish_year") or "Unknown", "Editions": book.get("edition_count", "Unknown"),
                     "Link": "https://openlibrary.org" + key if key.startswith("/works/") else "Unavailable"})
    return report("Book discovery shortlist", {"Mode": "Live API" if args.live else "User JSON" if args.input else "Recorded API snapshot",
        "Query": args.query if not args.input else "Supplied JSON (query not verified)", "Books shown": len(rows)},
        ["Title", "Authors", "First publication", "Editions", "Link"], rows,
        ["Book metadata comes from Open Library; the sample is a real recorded response with provenance.json.",
         "Search order is API relevance, not a quality ranking. Missing metadata stays Unknown. A listing does not imply free full-text access.",
         "Live mode makes one request. Keep unidentified traffic below 1 request/second; identify regular use with OPENLIBRARY_CONTACT and follow provider terms."])
