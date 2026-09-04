"""Run one project or all ten demos. Python 3.11+, no dependencies."""

import argparse
import importlib.util
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

from toolkit import ROOT, ask_claude, claude_prompt, iso_date, markdown, read_json


def load_project(project):
    spec = importlib.util.spec_from_file_location(project["id"], ROOT / "projects" / project["folder"] / "app.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def execute(project, args):
    data = load_project(project).run(args)
    data["title"] = project.get("simple_title", data["title"])
    data["sources"] = project["sources"]
    if hasattr(args, "live"):
        if args.live:
            data["summary"]["Retrieved (UTC)"] = datetime.now(timezone.utc).isoformat()
        elif args.input is None:
            provenance = read_json(ROOT / "projects" / project["folder"] / "provenance.json")
            data["data_provenance"] = provenance
            data["summary"]["Snapshot retrieved (UTC)"] = provenance["retrieved_at_utc"]
            data["sources"] = [*data["sources"], {"title": "Recorded data endpoint", "url": provenance["source_url"]}]
    destination = args.output_dir
    destination.mkdir(parents=True, exist_ok=True)
    stem = destination / project["id"]
    text = markdown(data)
    stem.with_suffix(".md").write_text(text, encoding="utf-8")
    stem.with_suffix(".json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    prompt = claude_prompt(project, data)
    stem.with_suffix(".prompt.md").write_text(prompt, encoding="utf-8")
    if args.claude:
        stem.with_suffix(".claude.md").write_text(ask_claude(prompt), encoding="utf-8")
    print(text)
    print(f"Saved reports and Claude prompt: {stem}.*\n")
    return data


def main(argv=None):
    catalog = read_json(ROOT / "catalog.json")
    parser = argparse.ArgumentParser(description="Techwitray: 10 practical projects to build with Claude")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="List the ten projects")
    demo = sub.add_parser("demo", help="Run all ten with offline samples; no API calls")
    demo.add_argument("--output-dir", type=Path, default=ROOT / "output")
    for project in catalog:
        child = sub.add_parser(project["id"], help=project["title"])
        child.add_argument("--output-dir", type=Path, default=ROOT / "output")
        child.add_argument("--claude", action="store_true", help="Send the resulting report to the paid Claude API for a draft")
        load_project(project).configure(child)
    args = parser.parse_args(argv)
    try:
        if args.command == "list":
            for project in catalog:
                print(f"{project['id']:12} {project['difficulty']:6} {project['title']}")
        elif args.command == "demo":
            for project in catalog:
                defaults = parser.parse_args([project["id"]])
                defaults.output_dir = args.output_dir
                if hasattr(defaults, "as_of"):
                    defaults.as_of = date(2026, 9, 4)
                execute(project, defaults)
        else:
            execute(next(item for item in catalog if item["id"] == args.command), args)
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    raise SystemExit(main())
