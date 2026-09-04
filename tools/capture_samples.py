"""Explicitly refresh the three bundled public API samples and record provenance."""
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from toolkit import ROOT, fetch_json

SAMPLES = [
    ("08-book-finder", "Open Library", "https://openlibrary.org/search.json?" + urlencode({
        "q": "python programming", "limit": 5, "fields": "key,title,author_name,first_publish_year,edition_count"}),
     "Open Library bibliographic metadata; see https://openlibrary.org/developers/licensing"),
    ("09-weather-planner", "Open-Meteo", "https://api.open-meteo.com/v1/forecast?" + urlencode({
        "latitude": 40.7128, "longitude": -74.0060,
        "daily": "temperature_2m_max,precipitation_probability_max,wind_speed_10m_max", "timezone": "auto", "forecast_days": 7,
        "temperature_unit": "celsius", "wind_speed_unit": "kmh"}),
     "Weather data by Open-Meteo.com, CC BY 4.0; https://open-meteo.com/en/terms"),
    ("10-repo-check", "GitHub public repository API", "https://api.github.com/repos/psf/requests",
     "Public repository metadata; upstream code and branding are not relicensed by this project."),
]


def main():
    for folder, provider, url, attribution in SAMPLES:
        data = fetch_json(url)
        content = (json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
        target = ROOT / "projects" / folder
        (target / "sample.json").write_bytes(content)
        provenance = {"provider": provider, "source_url": url, "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
                      "sha256": hashlib.sha256(content).hexdigest(), "transformation": "JSON formatting only; field values unchanged", "attribution": attribution}
        (target / "provenance.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")
        print(f"Captured {provider}: {len(content)} bytes")


if __name__ == "__main__":
    main()
