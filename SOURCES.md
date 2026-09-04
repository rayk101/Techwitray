# Source register

Sources checked 2026-09-04 (UTC). Sources inform the implementation; they do not endorse Techwitray.

Projects 1–7 use original, fictional business examples. Projects 8–10 include real API snapshots; each provenance.json records its exact URL, UTC retrieval time, transformation and SHA-256 checksum.

## 01 · Expense analyzer

- [CFPB — Your Money, Your Goals toolkit](https://www.consumerfinance.gov/consumer-tools/educator-tools/your-money-your-goals/toolkit/) — Real-world basis for tracking and categorizing spending; sample transactions and software are original.

## 02 · Freelancer invoice tracker

- [Stripe — Accounts receivable aging report](https://docs.stripe.com/revenue-recognition/reports/accounts-receivable-aging) — Explains outstanding balances grouped by age. Our simplified 90+ bucket combines Stripe's older ranges; this is not a Stripe integration.

## 03 · Inventory reorder planner

- [Shopify — Reorder point formula](https://www.shopify.com/blog/reorder-point) — Reorder point = demand during lead time + safety stock. Our review-interval order-up-to policy is an explicit project design choice.

## 04 · Support ticket triage

- [Atlassian — Understanding incident severity levels](https://www.atlassian.com/incident-management/kpis/severity-levels) — Real-world rationale for prioritization. The project's P1/P2/P3 keywords are original teaching rules, not Atlassian's severity taxonomy.

## 05 · Meeting action tracker

- [Atlassian — How to take useful meeting notes](https://www.atlassian.com/blog/teamwork/meeting-notes) — Motivation for recording actionable meeting outcomes. The parser's input syntax and sample meeting are original.

## 06 · Campaign link builder

- [Google Analytics — Collect campaign data with custom URLs](https://support.google.com/analytics/answer/10917952?hl=en) — Defines utm_source, utm_medium, utm_campaign and utm_content and explains case sensitivity. Lowercasing is our consistency policy.

## 07 · Resume and job skill comparison

- [U.S. Department of Labor — Resume Essentials participant guide](https://www.dol.gov/sites/dolgov/files/VETS/files/ResumeEssentials_PG_Interactive_Feb2026.pdf) — Supports targeted resume review and keyword/gap comparison. This tool's metric is not a validated ATS score.

## 08 · Book discovery shortlist

- [Open Library — Search API](https://openlibrary.org/dev/docs/api/search) — Endpoint, query fields and bibliographic metadata.
- [Open Library — API usage guidelines](https://openlibrary.org/developers/api) — Rate limits, identification and low-volume use requirements.

## 09 · Outdoor filming weather planner

- [Open-Meteo — Forecast API documentation](https://open-meteo.com/en/docs) — Daily variables, coordinates, timezone and units. Weather data attribution: Open-Meteo, CC BY 4.0.
- [Open-Meteo — Terms](https://open-meteo.com/en/terms) — Hosted free API usage limits and non-commercial-use terms.

## 10 · Public repository maintenance check

- [GitHub — Repository REST API](https://docs.github.com/en/rest/repos/repos#get-a-repository) — Public repository endpoint and returned metadata fields.
- [GitHub — REST API rate limits](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api) — Public unauthenticated request limits; this project makes one request per live run.

## Shared Claude integration

- [Anthropic Messages API](https://platform.claude.com/docs/en/api/messages/create) — request fields and response text blocks.
- [Anthropic API overview](https://platform.claude.com/docs/en/api/overview) — authentication and version headers.

## Attribution

Original code and fictional samples are MIT licensed. Provider data retains its own terms. Weather data by [Open-Meteo](https://open-meteo.com/), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Open Library records and GitHub metadata are attributed in their project folders; no full books, third-party code or source articles are reproduced.
