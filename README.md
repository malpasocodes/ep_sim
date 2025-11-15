# Earnings Premium Simulation – Version 1

This repository hosts Version 1 of the **Earnings Premium Simulation Tool**, a Streamlit app that uses synthetic data to show how college program pass/fail outcomes change when federal accountability rules rely on:

- a single **statewide high-school earnings benchmark**, versus  
- **local (commuting-zone) earnings benchmarks** that better reflect actual labor markets.

The goal is to make geographic bias in accountability metrics visible and intuitive for non-technical audiences.

## What the App Shows

- **State & simulation overview**
  - State-specific commuting-zone (CZ) counts based on a proportional mapping (`data/state_cz_mapping.csv`).
  - Programs per CZ and total simulated program count.
  - Within-state inequality setting (low/medium/high).

- **Local vs statewide earnings distribution**
  - Histogram of **local HS earnings** across CZs in the selected state.
  - Dashed vertical line for the **statewide HS median**.
  - Shows how many local labor markets sit below the statewide benchmark.

- **Benchmark sensitivity**
  - Scatterplot of `distance_local` vs `distance_state` for each program.
  - Programs classified into four groups:
    - Pass Both
    - Fail Both
    - Pass State Only
    - Pass Local Only (often the largest misclassified group).
  - Bar chart summarizing the share in each category.

- **Time horizon comparison**
  - Example program trajectories comparing **early** (3–4 year) vs **later** (10-year) earnings.
  - Overlaid benchmark line to show how “borderline” programs early on can move further above the benchmark over time.

## How It Works (Under the Hood)

- **Synthetic inputs**
  - State-level HS earnings medians (`simulation/config.py`).
  - State → CZ count mapping (`data/state_cz_mapping.csv`).
  - Within-state inequality parameter that widens/narrows local earnings around the state median.

- **Geography & programs**
  - `simulation/geo.py` synthesizes CZ objects per state with:
    - IDs, human-readable names, CZ types (urban/suburban/rural),
    - local HS earnings drawn from state medians + inequality settings.
  - `simulation/programs.py` generates 2‑year and 4‑year programs per CZ with early/later earnings bumps and noise.

- **Evaluation & visuals**
  - `simulation/evaluation.py` computes:
    - earnings relative to statewide and local benchmarks,
    - pass/fail flags and distances,
    - four-category classification.
  - `simulation/visuals.py` builds:
    - scatter + bar charts,
    - local-vs-state earnings histogram,
    - sample program trajectories,
    - narrative text tying the visuals together.

Everything runs in memory via Pandas/NumPy and updates reactively when sidebar controls change.

## Getting Started (Local Development)

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
4. **Docs**: `PRD.md`, `ProjectPlan.md`, `Tech_Specs.md`, `UI_UX_Spec.md`, `Additional_Visualizations_Spec.md`, `README_DEPLOY.md`, `Demo_Script.md`, and `docs/Interpretation_Guide.md` live at the root (or `/docs`) for quick reference.

## Deployment (Render)

The app is designed to run as a Render web service:

- Configuration lives in `render.yaml`.
- Typical settings:
  - **Build command:** `pip install -r requirements.txt`
  - **Start command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
  - **Env vars:** `PYTHON_VERSION=3.12.0`, optional `STREAMLIT_BROWSER_GAP=0`
- See `README_DEPLOY.md` for step‑by‑step instructions.

## Project Documentation & Design

- **Product & design**
  - `PRD.md` – Product Requirements (problem, goals, users).
  - `UI_UX_Spec.md` – UI layout and interaction model.
  - `Additional_Visualizations_Spec.md` – interpretability visualizations.
  - `docs/Interpretation_Guide.md` – “how to read” the app for non-technical audiences.

- **Technical**
  - `Tech_Specs.md` – architecture, data model, performance targets.
  - `ProjectPlan.md` – multi-phase implementation plan.
  - `Demo_Script.md` – suggested 5‑minute live demo script.

## Development History

The repository was built in ten phases (setup, config, CZ scaffolding, programs, evaluation, visuals, Streamlit UI, performance profiling, Render deployment, documentation + licensing). For more detail, see `ProjectPlan.md` and `dev_log.md`.

## License

Released under the [MIT License](LICENSE). Code and documentation are intended for public use via the GitHub repository and Render deployment described above.

---

Future versions will integrate real data (ACS, IPEDS, College Scorecard) and add richer filters (sector, demographics, MSI status) while preserving the interpretability focus of this prototype.
