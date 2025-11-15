# Earnings Premium Simulation – Version 1

This repository hosts the synthetic prototype described in the PRD. The application
is a Streamlit app that simulates how pass/fail results change when comparing
statewide high-school earnings benchmarks to local (commuting-zone) benchmarks.

## Phase 1 Status
- Repository initialized with placeholders for `simulation/`, `pages/`, and `utils/`.
- `app.py` is a Streamlit stub; later phases will add real simulation logic and UI components.
- Requirements file captures the baseline dependencies (Streamlit, Plotly, Pandas, NumPy).

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
