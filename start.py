"""A small, offline menu for beginners. Run with python start.py."""
import contextlib
import io
import sys

import run
from toolkit import ROOT, read_json


def main(output_dir=ROOT / "output"):
    projects = read_json(ROOT / "catalog.json")
    while True:
        print("\nTECHWITRAY - PICK A PROJECT\n")
        for number, project in enumerate(projects, 1):
            print(f"  {number:2}. {project['simple_title']}")
        print("\nThese examples use sample data. No accounts or keys needed.")
        choice = input("Choose 1-10, or q to quit: ").strip().lower()
        if choice == "q":
            return 0
        if choice not in {str(number) for number in range(1, len(projects) + 1)}:
            print("Please type a number from 1 to 10, or q.")
            continue
        project = projects[int(choice) - 1]
        arguments = project["demo"].split()[2:] + ["--output-dir", str(output_dir)]
        with contextlib.redirect_stdout(io.StringIO()):
            status = run.main(arguments)
        if status:
            print("The example could not run. Copy the error above if you need help.")
        else:
            data = read_json(output_dir / (project["id"] + ".json"))
            print(f"\n{project['simple_title'].upper()}\n")
            for label, value in data["summary"].items():
                if "retrieved" not in label.lower():
                    print(f"{label}: {value}")
            print()
            for row in data["rows"]:
                print(" - " + " | ".join(f"{field}: {row[field]}" for field in project["preview_fields"]))
            print(f"\nSaved in output/{project['id']}.md")
            print("\nTry next: " + project["small_change"])
        input("\nPress Enter to return to the menu.")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    try:
        raise SystemExit(main())
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
