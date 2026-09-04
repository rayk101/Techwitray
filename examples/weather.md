# Outdoor filming weather planner

*Techwitray · practical projects to build with Claude*

- **Mode:** Recorded forecast — not current
- **Forecast timezone:** America/New_York
- **Days fitting preferences:** 6
- **Snapshot retrieved (UTC):** 2026-09-04T03:29:14.193459+00:00

| Date | High (C) | Max rain probability (%) | Max wind (km/h) | Filming preference |
| --- | --- | --- | --- | --- |
| 2026-09-03 | 30.0 | 80 | 18.1 | Backup plan |
| 2026-09-04 | 29.5 | 30 | 23.2 | Fits |
| 2026-09-05 | 25.9 | 22 | 18.7 | Fits |
| 2026-09-06 | 23.6 | 22 | 20.0 | Fits |
| 2026-09-07 | 26.6 | 2 | 14.0 | Fits |
| 2026-09-08 | 28.0 | 1 | 15.2 | Fits |
| 2026-09-09 | 23.1 | 30 | 13.7 | Fits |

## Notes

- Preference: daily max rain probability &lt;= 30% and max wind &lt;= 25 km/h. These are project defaults, not safety thresholds.
- Weather data by Open-Meteo.com, CC BY 4.0. Sample is an unchanged recorded API response; see provenance.json for retrieval time and coordinates.
- Daily maxima do not identify a dry time slot. Forecasts change; this is not a warning or safety service. Use --live for a fresh forecast.
- Open-Meteo&#x27;s free hosted API is for non-commercial use; check the linked terms before commercial deployment.

## Sources

- [Open-Meteo — Forecast API documentation](https://open-meteo.com/en/docs)
- [Open-Meteo — Terms](https://open-meteo.com/en/terms)
- [Recorded data endpoint](https://api.open-meteo.com/v1/forecast?latitude=40.7128&longitude=-74.006&daily=temperature_2m_max%2Cprecipitation_probability_max%2Cwind_speed_10m_max&timezone=auto&forecast_days=7&temperature_unit=celsius&wind_speed_unit=kmh)
