# Techwitray reel kit

## Hook

“10 practical projects you can build with Claude — with working code and real sources.”

Use this wording for the delivered starters. Avoid claiming they landed job offers or generated income unless you have your own evidence. This repository was assembled with AI assistance; the prompts let viewers build and extend it with Claude.

## 45-second shot list

| Time | Visual | Voiceover / overlay |
| --- | --- | --- |
| 0–3s | Root README and all ten project links | “Stop collecting project ideas. Build something you can actually run.” |
| 3–6s | Expense report category table | “One: analyze a bank CSV.” |
| 6–9s | Overdue invoice rows | “Two: track unpaid freelance invoices.” |
| 9–12s | Inventory reorder quantities | “Three: plan a shop's next restock.” |
| 12–15s | Support queues and evidence | “Four: triage support tickets.” |
| 15–18s | Action owners and missing date | “Five: turn meeting notes into a checklist.” |
| 18–21s | Campaign URL with UTM parameters | “Six: build tracking links for your content.” |
| 21–24s | Resume skill evidence and gaps | “Seven: compare your resume with a job posting.” |
| 24–27s | Real Open Library titles and links | “Eight: find books through a real API.” |
| 27–30s | Dated live forecast and preference label | “Nine: plan outdoor filming around the forecast.” |
| 30–33s | Repo metadata checklist | “Ten: check a public GitHub repo.” |
| 33–39s | Edit one sample value and rerun the command | “Each one includes code, a demo, source links, and a prompt to build on it with Claude.” |
| 39–45s | Repo URL and project table | “Easy to medium. Grab Techwitray from the link in my bio.” |

## Record actual output

```bash
python run.py demo
python run.py inventory
python run.py weather --live
python run.py repocheck --live --repo rayk101/Techwitray
```

Open `output/inventory.md` in a Markdown preview and zoom in. Change STK-03 on_hand from 12 to 24 in a copy of the CSV, run `python run.py inventory --input your-copy.csv`, and show the order suggestion moving from 60 to 48. This demonstrates a real calculation.

For weather, display the dates and mode label. If you film a bundled sample, keep “Recorded forecast — not current” visible. Business examples are fictional; show them as demos. Crop or hide terminals containing environment variables, personal directories or private data.

## Caption

10 practical projects to build with Claude. Easy-to-medium scope, runnable Python code, sample inputs, real API examples and source links. Start with one, change it, test it, and be ready to explain how it works.

Code: https://github.com/rayk101/Techwitray#user-content-start-here

#Techwitray #ClaudeAI #PythonProjects #BuildInPublic #LearnToCode

## Pinned comment

Repo: https://github.com/rayk101/Techwitray#user-content-start-here — all 10 projects have a README, code, example output, source links and a Claude prompt. The default demos run without an API key.
