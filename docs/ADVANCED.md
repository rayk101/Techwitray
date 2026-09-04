# Extra details

You can skip this page when starting out.

## More ways to run a project

```bash
python run.py list
python run.py demo
python run.py expenses --month 2026-08
python run.py expenses --input my-transactions.csv --month 2026-08
```

Use `python3` instead of `python` on Mac/Linux if needed. `--help` shows each project's options. Each project folder has a `DETAILS.md` with its input format, calculations and sources.

The `output` folder contains readable `.md` reports, `.json` data and `.prompt.md` text you can paste into Claude. The all-project demo uses 2026-09-04 as a fixed reference date. Individual date-based commands use today unless you supply `--as-of`.

## Fresh public data

The menu uses saved examples. These commands fetch new data:

```bash
python run.py books --live --query "python programming" --limit 5
python run.py weather --live --latitude 40.7128 --longitude -74.0060
python run.py repocheck --live --repo rayk101/Techwitray
```

Real sample files have a `provenance.json` recording where and when the data was collected. [Sources and provider terms](../SOURCES.md).

Open Library asks for low-volume use and identification for regular requests. GitHub limits public API requests. Open-Meteo's free hosted endpoint is for non-commercial use; check its terms before commercial deployment.

## Optional Claude connection

[API setup](CLAUDE_API.md) is available if you want the code to send reports directly to Claude. It requires separate credentials and can cost money. Copying the prompt into your usual Claude chat is the simpler starting point.

## Check the code

```bash
python -m unittest discover -s tests -v
```

[Verification notes](VERIFICATION.md) explain what was tested. The initial paid Claude request was not live-tested; its request and response handling has mocked tests.

## Updating this collection

Edit `catalog.json` and run `python tools/build_docs.py` to refresh the guides. `python tools/capture_samples.py` refreshes the three public-data samples. Regenerate examples with `python run.py demo --output-dir examples` after changing samples or report formatting.

Original code and fictional examples are [MIT licensed](../LICENSE). External data keeps its own terms. This independent collection is not endorsed by Anthropic or the source providers, and it makes no hiring or income claims.

[Back to the projects](../README.md)
