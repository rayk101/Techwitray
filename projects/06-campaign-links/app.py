"""Build correctly encoded campaign URLs from a batch CSV."""
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from toolkit import read_csv, report


def configure(parser):
    parser.add_argument("--input", type=Path, default=Path(__file__).with_name("sample.csv"))


def build_url(url, source, medium, campaign, content=""):
    parts = urlsplit(url)
    if parts.scheme not in ("https", "http") or not parts.hostname or parts.username or parts.password:
        raise ValueError("Destination must be an absolute HTTP(S) URL without credentials")
    if any(char.isspace() for char in url):
        raise ValueError("URL must not contain unencoded whitespace")
    # Replace existing UTM fields while retaining unrelated query parameters and fragments.
    query = [(key, value) for key, value in parse_qsl(parts.query, keep_blank_values=True) if not key.lower().startswith("utm_")]
    for name, value in (("source", source), ("medium", medium), ("campaign", campaign)):
        value = value.strip().lower()
        if not value:
            raise ValueError(f"Campaign {name} must not be blank")
        query.append(("utm_" + name, value))
    if content.strip():
        query.append(("utm_content", content.strip().lower()))
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def run(args):
    records = read_csv(args.input, ["url", "source", "medium", "campaign"])
    rows = [{"Source": row["source"].lower(), "Medium": row["medium"].lower(), "Campaign": row["campaign"].lower(),
             "URL": build_url(row["url"], row["source"], row["medium"], row["campaign"], row.get("content", ""))} for row in records]
    return report("Campaign link builder", {"Links generated": len(rows)}, ["Source", "Medium", "Campaign", "URL"], rows,
        ["Fictional campaigns using example.com. Replace it with your landing page before sharing.",
         "UTM values are normalized to lowercase. Existing utm_* parameters are replaced; other parameters and #fragments are preserved.",
         "URLs are generated locally, not visited. Analytics tracking must already be configured on the destination to measure results."])
