# Earnings Premium Simulation – Version 1

This repository hosts the synthetic prototype described in the PRD. The application
is a Streamlit app that simulates how pass/fail results change when comparing
statewide high-school earnings benchmarks to local (commuting-zone) benchmarks.

## Phase 1 Status
- Repository initialized with placeholders for `simulation/`, `pages/`, and `utils/`.
- `app.py` is a Streamlit stub; later phases will add real simulation logic and UI components.
- Requirements file captures the baseline dependencies (Streamlit, Plotly, Pandas, NumPy).

## Phase 2 Progress
- Added `simulation/config.py` with centralized definitions for time horizons, program bump ranges, inequality slider behavior, state-level synthetic HS earnings, and commuting-zone assumptions.
- Exposed helper utilities (`inequality_std`, `get_state_hs_earnings`, `SIM_DEFAULTS`) so later modules can stay lightweight.

## Phase 3 Progress
- Added `data/commuting_zones.csv`, a synthetic crosswalk listing two commuting zones (urban + rural) for every state + DC.
- Implemented `simulation/geo.py` which ingests the crosswalk, assigns local HS earnings based on state medians + inequality slider, and returns dataclass-backed `State`/`CommutingZone` objects for downstream program generation.

## Phase 4 Progress
- Added `simulation/programs.py` with a `Program` dataclass and generator routine that creates synthetic two-year/four-year programs per CZ using the bump ranges defined in `config`.
- Included helper utilities for downstream pandas integration (`programs_to_records`) so later phases can build evaluation DataFrames quickly.

## Phase 5 Progress
- Added `simulation/evaluation.py` with functions that compute state/local benchmark distances, pass/fail flags, and classification labels for each program based on a selected time horizon.
- Included `summarize_classifications` helper to produce counts/shares for the bar chart planned in later UI phases.

## Phase 6 Progress
- Added `simulation/visuals.py` (Plotly helpers) to render the distance scatterplot, classification bar chart, and a short narrative summary using the evaluation outputs.
- Confirmed the visuals create Plotly `Figure` objects via a quick end-to-end smoke test (states → programs → eval → charts).

## Phase 7 Progress
- Replaced the placeholder `app.py` with a working Streamlit UI that wires together the state/CZ generator, program simulation, evaluation logic, and Plotly visuals. Sidebar controls expose state filter, horizon, inequality slider, programs-per-CZ, and random seed.
- Cached heavy computations via `st.cache_data` to keep interactions fast; added a raw data preview to help validate results.

## Phase 8 Progress
- Added `watchdog` to enable Streamlit's file watcher and ran performance profiling (6,120 programs evaluated in ~11 ms, 8,160 programs in ~10.8 ms) showing well under the 1s requirement.
- Documented profiling approach and noted that no further optimizations were required thanks to vectorized pandas operations.

## Development notes
1. **Environment management**: use [`uv`](https://github.com/astral-sh/uv) for creating the virtual environment and installing dependencies:
   ```bash
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```
2. **Running the app locally**:
   ```bash
   streamlit run app.py
   ```
3. **Code organization**:
   - `simulation/`: configuration, synthetic data rules, evaluation logic (Phases 2–5)
   - `pages/`: Streamlit multipage entries (Phase 7)
   - `utils/`: shared helpers (logging, formatting, etc.)
4. **Docs**: `PRD.md`, `ProjectPlan.md`, `Tech_Specs.md`, and `UI_UX_Spec.md` live at the root for quick reference.

Future phases will follow the project plan to flesh out the simulation engine, Plotly
visuals, Streamlit layout, performance optimizations, and deployment to Render.
