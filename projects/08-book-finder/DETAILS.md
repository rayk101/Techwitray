# 08 · Book discovery shortlist

**Medium · 3–4 hours to rebuild and customize** · [All projects](../../README.md)

Search real book metadata and export a linked reading shortlist.

[Source code](app.py) · [Sample input](sample.json) · [Example report](../../examples/books.md) · [Claude build prompt](PROMPT.md)

## Run

From the repository root, with Python 3.11 or newer:

```bash
python run.py books
```

Reports are written to output/books.md and .json. The .prompt.md file contains the actual report and a tailored analysis request for Claude. All default demos work offline.

Fetch current public data:

```bash
python run.py books --live --query "python programming" --limit 5
```

The bundled JSON is a recorded snapshot, not current data. [Inspect its provenance](provenance.json).

## Use your own input

Offline: recorded Open Library JSON snapshot. Live: a query and limit of 1–20. --input accepts another API search response; query is not inferred from that file.

```bash
python run.py books --input path/to/your-file.json
```

## What the code does

Makes one search request with explicit fields, handles missing author/year metadata and returns work-page links. Default mode makes no network calls.

## Reel demo

Show actual titles, authors and clickable Open Library records; run --live with a different subject.

## Claude analysis

Format these records as a readable shortlist with the supplied links. You have titles and bibliographic metadata, not book contents; do not invent summaries, reviews or recommendations based on unseen text.

Copy output/books.prompt.md into Claude, or see the [optional API setup](../../docs/USING_CLAUDE.md). The report is calculated by Python; model text is a separate draft.

## Take it further

Add local caching and a saved reading-list file. Use the API's subject fields before asking Claude to organize books by topic.

## Sources and scope

- [Open Library — Search API](https://openlibrary.org/dev/docs/api/search): Endpoint, query fields and bibliographic metadata.
- [Open Library — API usage guidelines](https://openlibrary.org/developers/api): Rate limits, identification and low-volume use requirements.

Review the notes in the [example report](../../examples/books.md) for assumptions and limitations.
