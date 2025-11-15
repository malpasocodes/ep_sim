# Development Log

## 2025-11-15
- Established Phase 1 scaffolding (folders, placeholder Streamlit app, base requirements, gitignore, README).
- Documented current status and next steps for follow-on phases.
- Initialized the project with `uv` and created a `.venv` for local development.
- Added `simulation/config.py` capturing time horizons, program bump logic, inequality slider mapping, state-level HS benchmarks, and CZ/program defaults for upcoming phases.
- Created `data/commuting_zones.csv` (urban + rural CZ entries per state/DC) and `simulation/geo.py` to generate state/commuting-zone objects with synthetic local HS earnings informed by inequality settings.
- Phase 3 complete; next up is Phase 4 (program generator) to populate synthetic 2-yr/4-yr programs per CZ.
