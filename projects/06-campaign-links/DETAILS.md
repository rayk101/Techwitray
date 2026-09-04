# 06 · Campaign link builder

**Easy · 1–2 hours to rebuild and customize** · [All projects](../../README.md)

Generate consistent tracking links for reels, newsletters and videos.

[Source code](app.py) · [Sample input](sample.csv) · [Example report](../../examples/campaigns.md) · [Claude build prompt](PROMPT.md)

## Run

From the repository root, with Python 3.11 or newer:

```bash
python run.py campaigns
```

Reports are written to output/campaigns.md and .json. The .prompt.md file contains the actual report and a tailored analysis request for Claude. All default demos work offline.

## Use your own input

CSV: url,source,medium,campaign; optional content. Supply absolute HTTP(S) destination URLs. Example.com is a demo destination.

```bash
python run.py campaigns --input path/to/your-file.csv
```

## What the code does

URL-encodes campaign values, normalizes UTM values to lowercase, replaces existing utm_* fields and preserves other parameters and fragments.

## Reel demo

Show the Instagram URL preserving ref=profile and #signup while adding campaign parameters.

## Claude analysis

Review the generated campaign names for consistency and suggest two clearly labeled alternative utm_content naming conventions. Do not claim clicks, conversions or analytics setup have been verified.

Copy output/campaigns.prompt.md into Claude, or see the [optional API setup](../../docs/USING_CLAUDE.md). The report is calculated by Python; model text is a separate draft.

## Take it further

Add approved source/medium presets and a duplicate-campaign-name checker. Verify attribution on your own analytics-enabled landing page.

## Sources and scope

- [Google Analytics — Collect campaign data with custom URLs](https://support.google.com/analytics/answer/10917952?hl=en): Defines utm_source, utm_medium, utm_campaign and utm_content and explains case sensitivity. Lowercasing is our consistency policy.

Review the notes in the [example report](../../examples/campaigns.md) for assumptions and limitations.
