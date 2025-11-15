# Project Plan  
## Earnings Premium Simulation – Version 1  
### EDU Accountability Lab  
### 10‑Phase Development Plan

---

## **1. Introduction**

This project plan outlines ten clear, sequential phases for developing Version 1 of the Earnings Premium Simulation Tool. Version 1 relies entirely on synthetic data but uses real commuting zones and realistic assumptions. Each phase includes core tasks, goals, and expected deliverables. The plan is designed for iterative building using Code, Streamlit, and Render, with a focus on shipping a polished, credible prototype suitable for policymakers.

---

# **Phase 1 – Project Setup & Repository Initialization**
**Goal:** Establish the development environment and file structure.  
**Tasks:**  
- Create Git repository and folders (`simulation/`, `pages/`, `utils/`).  
- Add placeholder `app.py`, `requirements.txt`, and `.gitignore`.  
- Write basic README with development notes.  
**Deliverables:**  
- Clean repo aligned with Tech Specs.

---

# **Phase 2 – Define Simulation Parameters & Synthetic Data Rules**
**Goal:** Lock in all variable definitions and synthetic-data assumptions.  
**Tasks:**  
- Implement constants for: time horizons, earnings multipliers, inequality distribution.  
- Define synthetic values for statewide HS earnings.  
- Define distributions for local earnings per commuting zone.  
**Deliverables:**  
- `simulation/config.py` containing all model parameters.

---

# **Phase 3 – Build the Commuting Zone Structure**
**Goal:** Build the geographic scaffolding (states + CZs).  
**Tasks:**  
- Load a predefined CSV listing commuting zones and their states.  
- Build Python structures: `State`, `CommutingZone` classes.  
- Assign synthetic HS earnings to each CZ based on state values + inequality.  
**Deliverables:**  
- Functional CZ/state generator with realistic synthetic structure.

---

# **Phase 4 – Generate Synthetic Programs**
**Goal:** Create synthetic 2‑year and 4‑year programs within each CZ.  
**Tasks:**  
- Define number of programs per CZ (user‑controlled).  
- Assign program type (random or proportional).  
- Generate early‑career and later‑career earnings using rules defined earlier.  
**Deliverables:**  
- `simulation/program_generator.py` producing a list of synthetic programs.

---

# **Phase 5 – Implement Benchmark Comparison Logic**
**Goal:** Compute pass/fail for each program under statewide and local benchmarks.  
**Tasks:**  
- Implement distance calculations for both benchmarks.  
- Implement pass/fail flags.  
- Implement 4-category classification (pass both, fail both, pass state only, pass local only).  
**Deliverables:**  
- `simulation/evaluation.py` computing outcomes as a DataFrame.

---

# **Phase 6 – Build the Visualization Layer (Plotly)**
**Goal:** Implement the two main UI visualizations with synthetic data.  
**Tasks:**  
- Quadrant scatterplot (distance_local vs distance_state).  
- Bar chart summarizing classification categories.  
- Narrative generator summarizing results in plain English.  
**Deliverables:**  
- `visuals.py` or integrated UI components callable from Streamlit.

---

# **Phase 7 – Streamlit UI Integration**
**Goal:** Build the front-end page and wire up controls.  
**Tasks:**  
- Sidebar controls: state, horizon, inequality slider, num programs.  
- Render scatterplot, bar chart, and summary narrative.  
- Ensure layout matches existing EDU Accountability Lab design language.  
**Deliverables:**  
- Complete Streamlit page: `pages/05_Earnings_Premium_Simulation.py`.

---

# **Phase 8 – Performance Optimization & Testing**
**Goal:** Ensure smooth execution (<1 second per simulation).  
**Tasks:**  
- Replace slow loops with vectorized pandas operations.  
- Stress-test with large synthetic datasets.  
- Run UI tests to ensure responsiveness.  
**Deliverables:**  
- Optimized code with documented profiling notes.

---

# **Phase 9 – Deploy to Render**
**Goal:** Launch the working prototype publicly.  
**Tasks:**  
- Configure Render web service.  
- Add start command:  
  `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`  
- Push code and test deployment.  
- Monitor logs and fix deployment issues.  
**Deliverables:**  
- Public URL for Version 1 of the tool.

---

# **Phase 10 – Documentation, Demo Script & Handoff**
**Goal:** Produce polished written and verbal materials for demos.  
**Tasks:**  
- Update README with user instructions.  
- Write a 1–2 page “How to Interpret Results” brief.  
- Prepare a short live-demo script for policymakers.  
- Archive synthetic assumptions for future versions.  
**Deliverables:**  
- Complete documentation package ready for presentations and v2 expansion.

---

# **End of Project Plan**

