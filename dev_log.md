# Development Log

## 2025-11-15
- Established Phase 1 scaffolding (folders, placeholder Streamlit app, base requirements, gitignore, README).
- Documented current status and next steps for follow-on phases.
- Initialized the project with `uv` and created a `.venv` for local development.
- Added `simulation/config.py` capturing time horizons, program bump logic, inequality slider mapping, state-level HS benchmarks, and CZ/program defaults for upcoming phases.
- Added `data/state_cz_mapping.csv` to control how many commuting zones each state receives, updated `simulation/geo.py` to synthesize CZs/types/earnings from that mapping + inequality slider, and surfaced per-state CZ counts in the UI caption.
- Phase 3 complete; next up is Phase 4 (program generator) to populate synthetic 2-yr/4-yr programs per CZ.
- Added `simulation/programs.py` with program dataclasses, generation logic (using bump ranges + noise), and helper converters for DataFrame ingestion; Phase 4 kicked off.
- Smoke-tested Phase 3–4 stack via `.venv/bin/python`: generated 204 programs across 51 states using default settings (confirmed env wiring after `uv pip install -r requirements.txt`).
- Built Phase 5 evaluation module (`simulation/evaluation.py`) to compute benchmark distances, pass/fail flags, classification labels, and summary counts; verified via quick pandas test script.
- Ready for Phase 6 (visualization layer) now that evaluation outputs are DataFrame-friendly.
- Added `simulation/visuals.py` (scatter, bar, narrative builders) and confirmed end-to-end run from geo → programs → evaluation → Plotly figures works via `.venv/bin/python`.
- Phase 7: replaced placeholder `app.py` with the full Streamlit experience (sidebar controls + cached simulation pipeline + Plotly charts + data preview); smoke-tested locally.
- Phase 8: installed `watchdog` to improve Streamlit reload performance, profiled evaluation path (6k–8k programs evaluated in ~10–11 ms), and confirmed we already meet the <1s responsiveness goal without further tuning.
- Implemented the Additional Visualizations spec (state overview card, local-vs-state earnings histogram, enhanced narrative, and sample program trajectories) so users can interpret assumptions before diving into the scatter/bar charts.
- Phase 9 kickoff: added `render.yaml` and `README_DEPLOY.md` with Render build/start commands, env vars, and testing checklist.
