"""Check repository Markdown file links without making network requests."""
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def main():
    failures = []
    count = 0
    for path in ROOT.rglob("*.md"):
        if any(part in (".git", "tmp", "output", ".venv") for part in path.relative_to(ROOT).parts):
            continue
        text = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
        for match in re.finditer(r"\]\(([^\s)]+)\)", text):
            link = match[1]
            if urlsplit(link).scheme or link.startswith("#"):
                continue
            target = (path.parent / unquote(link.split("#")[0])).resolve()
            count += 1
            if not target.exists():
                failures.append(f"{path.relative_to(ROOT)} -> {link}")
    if failures:
        raise SystemExit("Broken local links:\n" + "\n".join(failures))
    print(f"Checked {count} local Markdown links: all resolve.")


if __name__ == "__main__":
    main()
