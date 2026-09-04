# Verification

Initial local verification: **2026-09-04 UTC**, Windows, Python 3.12.

| Check | Result |
| --- | --- |
| All ten offline demos | Passed; 10 Markdown reports, 10 JSON reports and 10 Claude-ready prompts generated |
| Behavioral and integration suite | 35 tests passed |
| Open Library live search | Passed with query `data science`, limit 3 |
| Open-Meteo live forecast | Passed with Los Angeles coordinates, seven daily rows |
| GitHub live metadata | Passed with `pallets/flask` |
| Recorded API data | Three sample checksums match their provenance files |
| Paid Anthropic API | Not run; missing configuration, request structure, response parsing and truncation are tested with mocks |

Run the same offline checks:

```bash
python -m unittest discover -s tests -v
python run.py demo
```

The all-project integration test blocks `urllib.request.urlopen` and verifies that every default demo still produces its output. Live checks were separate, explicit requests. Passing a mocked Claude test verifies the HTTP contract used by this client; it does not establish live model access or response quality.

The [GitHub Actions workflow](../.github/workflows/test.yml) repeats tests and demos on Python 3.11 and 3.12 on Ubuntu and Windows. [See the latest results](https://github.com/rayk101/Techwitray/actions/workflows/test.yml).

Beginner guide update: 36 tests passed locally, including every menu choice and recovery from invalid choices. The Windows launcher was also run successfully. All 192 local documentation links resolved.

The projects intentionally have small scopes: explicit spending categories; single-currency invoice balances; constant inventory demand; heuristic ticket routing; marked meeting actions; UTM generation without analytics setup; literal resume keyword matching; book metadata only; daily forecast preferences; and repository metadata only. These limits are also documented beside each output.
