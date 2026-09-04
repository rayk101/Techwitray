# 09 · Outdoor filming weather planner

**Medium · 3–5 hours to rebuild and customize** · [All projects](../../README.md)

Find forecast days that fit your rain and wind preferences for filming.

[Source code](app.py) · [Sample input](sample.json) · [Example report](../../examples/weather.md) · [Claude build prompt](PROMPT.md)

## Run

From the repository root, with Python 3.11 or newer:

```bash
python run.py weather
```

Reports are written to output/weather.md and .json. The .prompt.md file contains the actual report and a tailored analysis request for Claude. All default demos work offline.

Fetch current public data:

```bash
python run.py weather --live --latitude 40.7128 --longitude -74.0060 --max-rain 30 --max-wind 25
```

The bundled JSON is a recorded snapshot, not current data. [Inspect its provenance](provenance.json).

## Use your own input

Offline: recorded New York City forecast. Live: latitude/longitude, rain probability threshold (%) and wind threshold (km/h). --input accepts equivalent Open-Meteo JSON in Celsius, km/h and percent.

```bash
python run.py weather --input path/to/your-file.json
```

## What the code does

Fetches seven daily forecasts, validates parallel arrays and units, preserves unknown values and marks days fitting both preferences. Does not choose an hourly filming slot.

## Reel demo

Show dated forecast rows, then adjust --max-rain and see the preference labels change.

## Claude analysis

Draft a filming plan using only dates that fit the stated preferences. If none fit, say so. Never describe a day as safe or invent hourly conditions. Clearly distinguish a recorded snapshot from a live forecast.

Copy output/weather.prompt.md into Claude, or see the [optional API setup](../../docs/USING_CLAUDE.md). The report is calculated by Python; model text is a separate draft.

## Take it further

Add hourly daylight filtering and a location search. Include the forecast retrieval time in any calendar draft and review it before scheduling.

## Sources and scope

- [Open-Meteo — Forecast API documentation](https://open-meteo.com/en/docs): Daily variables, coordinates, timezone and units. Weather data attribution: Open-Meteo, CC BY 4.0.
- [Open-Meteo — Terms](https://open-meteo.com/en/terms): Hosted free API usage limits and non-commercial-use terms.

Review the notes in the [example report](../../examples/weather.md) for assumptions and limitations.
