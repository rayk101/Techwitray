"""Rank forecast days against an outdoor filming preference."""
from pathlib import Path
from urllib.parse import urlencode
import math

from toolkit import fetch_json, read_json, report

ENDPOINT = "https://api.open-meteo.com/v1/forecast"
VARIABLES = "temperature_2m_max,precipitation_probability_max,wind_speed_10m_max"


def configure(parser):
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--live", action="store_true")
    mode.add_argument("--input", type=Path, help="Use an Open-Meteo JSON response")
    parser.add_argument("--latitude", type=float, default=40.7128)
    parser.add_argument("--longitude", type=float, default=-74.0060)
    parser.add_argument("--max-rain", type=float, default=30)
    parser.add_argument("--max-wind", type=float, default=25, help="km/h")


def run(args):
    if not all(math.isfinite(value) for value in (args.latitude, args.longitude, args.max_rain, args.max_wind)):
        raise ValueError("Coordinates and thresholds must be finite")
    if not -90 <= args.latitude <= 90 or not -180 <= args.longitude <= 180:
        raise ValueError("Coordinates are out of range")
    if not 0 <= args.max_rain <= 100 or args.max_wind < 0:
        raise ValueError("Rain threshold must be 0-100; wind threshold must be nonnegative")
    params = {"latitude": args.latitude, "longitude": args.longitude, "daily": VARIABLES, "timezone": "auto", "forecast_days": 7,
              "temperature_unit": "celsius", "wind_speed_unit": "kmh"}
    if args.live:
        data = fetch_json(ENDPOINT + "?" + urlencode(params))
    else:
        if not args.input and (args.latitude != 40.7128 or args.longitude != -74.0060):
            raise ValueError("Different coordinates require --live; the bundled snapshot is for New York City")
        data = read_json(args.input or Path(__file__).with_name("sample.json"))
    daily = data["daily"]
    keys = ["time"] + VARIABLES.split(",")
    if len({len(daily[key]) for key in keys}) != 1:
        raise ValueError("Daily weather arrays have mismatched lengths")
    units = data.get("daily_units", {})
    if units.get("wind_speed_10m_max") != "km/h" or units.get("temperature_2m_max") != "°C" or units.get("precipitation_probability_max") != "%":
        raise ValueError("Expected forecast units: Celsius, km/h, and percent")
    rows = []
    for day, temp, rain, wind in zip(*(daily[key] for key in keys)):
        missing = any(value is None for value in (temp, rain, wind))
        fits = not missing and rain <= args.max_rain and wind <= args.max_wind
        rows.append({"Date": day, "High (C)": temp if temp is not None else "Unknown",
                     "Max rain probability (%)": rain if rain is not None else "Unknown", "Max wind (km/h)": wind if wind is not None else "Unknown",
                     "Filming preference": "Unknown" if missing else "Fits" if fits else "Backup plan"})
    return report("Outdoor filming weather planner", {"Mode": "Live forecast" if args.live else "User JSON" if args.input else "Recorded forecast — not current",
        "Forecast timezone": data.get("timezone", "Unknown"), "Days fitting preferences": sum(row["Filming preference"] == "Fits" for row in rows)},
        ["Date", "High (C)", "Max rain probability (%)", "Max wind (km/h)", "Filming preference"], rows,
        [f"Preference: daily max rain probability <= {args.max_rain:g}% and max wind <= {args.max_wind:g} km/h. These are project defaults, not safety thresholds.",
         "Weather data by Open-Meteo.com, CC BY 4.0. Sample is an unchanged recorded API response; see provenance.json for retrieval time and coordinates.",
         "Daily maxima do not identify a dry time slot. Forecasts change; this is not a warning or safety service. Use --live for a fresh forecast.",
         "Open-Meteo's free hosted API is for non-commercial use; check the linked terms before commercial deployment."])
