# Technical Specifications  
## Earnings Premium Simulation – Version 1  
### EDU Accountability Lab

---

## 1. Technical Overview

Version 1 of the Earnings Premium Simulation Tool is a Python-based Streamlit web application deployed on Render. It uses synthetic data and a simple simulation engine to model how program pass/fail outcomes differ when evaluated against statewide versus local high-school earnings benchmarks. The tool is intentionally lightweight, modular, and designed for future integration with real institutional data.

The architecture separates the simulation logic from the user interface, ensuring that later versions can replace synthetic data without altering the UI infrastructure.

Deployment is handled through a Render web service, and all Python dependencies/virtual environments are managed with `uv`.

---

## 2. System Architecture

The system follows a two-layer architecture:

### Application Layer (Streamlit UI)
- Implements the user interface, page layout, sidebar controls, and visualizations.
- Receives user input (state selection, time horizon, inequality slider).
- Calls simulation functions to regenerate results.
- Renders Plotly charts and narrative summaries.
- Runs entirely client-facing on Render.

### Simulation Engine (Python)
- Generates synthetic states, commuting zones, and program data.
- Computes early- and later-career earnings.
- Applies statewide and local benchmark comparisons.
- Produces a unified DataFrame for UI consumption.

All heavy lifting occurs in-memory using Pandas and NumPy, ensuring fast refresh.

---

## 3. Technology Stack

### Core Languages & Frameworks
- **Python 3.10+**
- **Streamlit** (UI framework)
- **Plotly** (interactive charts)
- **Pandas** (tabular data manipulation)
- **NumPy** (numeric operations)
- **uv** (package manager + virtual environment tooling)

### Deployment
- **Render Web Service**
  - Package management + env creation handled via `uv` (e.g., `uv pip install -r requirements.txt` within an `uv venv`)
  - Start: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

### Optional Libraries
- `pydantic` (optional for structured data models)
- `scikit-learn` (optional if generating distributions from templates)

---

## 4. Data Model & Structures

### 4.1 Core Entities

#### **State**
Fields:
- `state_name` (string)
- `state_hs_earnings` (float)
- `cz_list` (list of commuting zones)

#### **Commuting Zone (CZ)**
Fields:
- `cz_id` (string)
- `local_hs_earnings` (float)
- `cz_type` (categorical: urban/suburban/rural)
- `programs` (list of programs)

#### **Program**
Fields:
- `program_id` (string)
- `program_type` (two_year / four_year)
- `cz_id` (foreign key)
- `early_earnings` (float)
- `late_earnings` (float)

### 4.2 Output DataFrame (Primary UI Input)
Columns:
- `state`
- `cz_id`
- `cz_type`
- `state_hs_earnings`
- `local_hs_earnings`
- `program_id`
- `program_type`
- `early_earnings`
- `late_earnings`
- `benchmark_state_pass`
- `benchmark_local_pass`
- `distance_state`
- `distance_local`
- `classification_category`

This DataFrame drives all charts and tables.

---

## 5. Simulation Logic

### Step 1: Initialize States & Commuting Zones
- Load a predefined list of U.S. states and commuting zones (CZ identifiers only).
- Assign each state a synthetic high-school earnings value.
- Generate local HS earnings per CZ based on an inequality parameter:
  - `local_hs = state_hs + random_offset`
  - Offsets scaled by the inequality slider (low → narrow, high → wide).

### Step 2: Generate Programs
- For each CZ, generate `N` synthetic programs.
- Assign each program a type (two-year or four-year).
- Compute earnings:
  - `early_earnings = local_hs * (1 + small_bump)`
  - `late_earnings = local_hs * (1 + larger_bump)`
- Add random noise for variability.

### Step 3: Apply Earnings Tests
For each program:
- Statewide Test: `early_or_late >= state_hs`
- Local Test: `early_or_late >= local_hs`
- Compute distances:
  - `distance_state = program_earnings - state_hs`
  - `distance_local = program_earnings - local_hs`

### Step 4: Classify Programs
Program classification:
- Pass Both
- Fail Both
- Pass Local Only
- Pass State Only

This classification feeds the summary bar chart and interpretation block.

---

## 6. User Interface Logic

### Sidebar Inputs
- `state_selector`
- `time_horizon` (radio)
- `inequality_slider`
- `num_programs`
- `highlight_distressed`

### UI Update Flow
1. User changes a control.
2. Streamlit reruns the script.
3. Simulation engine is called with new parameters.
4. Updated DataFrame flows into:
   - Scatterplot
   - Bar chart
   - Summary text

Streamlit’s reactive model handles re-rendering automatically.

---

## 7. Visualization Specifications

### Scatterplot (Plotly)
- X-axis: `distance_local`
- Y-axis: `distance_state`
- Color: program classification or CZ type
- Tooltip includes:
  - program type
  - local HS earnings
  - state HS earnings
  - early/late earnings
  - pass/fail outcomes

### Bar Chart (Plotly)
- Bars: four classification categories
- Data: count or percentage
- Optional coloring for distressed CZs

### Tables
- Summary table with counts and percentages
- Optionally sortable by earnings or category

---

## 8. Performance & Scalability

### Performance Targets
- Simulation run time < 1 second
- Memory footprint < 200MB on Render free/standard plan
- Avoid long loops—use vectorized pandas operations

### Scalability
- Designed to handle up to:
  - 10k simulated programs
  - 3k commuting zones
  - 50 states

---

## 9. Error Handling & Logging

### Error Handling
- Invalid inputs default to safe values.
- No external data dependencies → minimal runtime errors.
- Clear messages if rendering fails.

### Logging
- Basic print-level debug logs during development.
- No persistent logs in v1.

---

## 10. Security & Privacy

- No real institutional data processed in v1.
- No user authentication.
- No PII collected.
- Compliant with Render’s security constraints.

---

## 11. Future Technical Extensions (v2/v3)

- Replace synthetic data with real ACS-based HS earnings.
- Integrate IPEDS/College Scorecard institutional data.
- Add filters for institutional sector, Pell %, MSI status.
- Add map-based CZ visualizations.
- Store precomputed real-data simulation outputs for speed.

---

## **End of Technical Specifications**
