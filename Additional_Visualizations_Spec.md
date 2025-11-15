
# Additional Visualizations Specification  
## Earnings Premium Simulation – Version 1.5  
### EDU Accountability Lab

This document describes a set of **additional visualizations** that should be added to the existing Streamlit app to help users understand the **assumptions** and **core variables** behind the simulation. The goal is to make the tool easier to interpret for non-technical users **before** they engage deeply with the main scatterplot and pass/fail mix chart.

These instructions are written for Codex to implement. They describe **what** to build and **where** to place it, not the exact code.

---

## 1. Layout Changes (High-Level)

1. Keep the current layout: sidebar on the left, main content on the right.  
2. In the main panel, introduce a new **"State & Simulation Overview"** section **above** the main scatterplot/bar-chart row.  
3. Below the overview, keep the existing two-column layout:
   - Left: benchmark distance scatterplot  
   - Right: pass/fail bar chart  

The new overview section will contain:

- A **summary card** showing key state-level counts.  
- A **distribution chart** of local high-school earnings vs statewide benchmark.  
- Optional explanatory text.

---

## 2. Visualization 1 – State & Simulation Summary Card

### Purpose

Give users an immediate sense of **how big and complex** the selected state is, and what the current simulation settings imply (number of commuting zones, total number of programs, etc.).

### Content

Create a card-style component at the top of the page with text along the lines of:

> **State Overview: Arkansas**  
> Commuting zones simulated: **10**  
> Programs per CZ: **35**  
> Total programs: **350**  
> Within-state inequality setting: **0.35 (medium)**  

### Implementation Notes for Codex

1. Calculate in Python (before rendering the plots):
   - `cz_count` for the selected state (already available via the new mapping).  
   - `programs_per_cz` from the slider.  
   - `total_programs = cz_count * programs_per_cz`.  
2. Use `st.container()` or `st.markdown()` with simple HTML/Markdown styling to render a bordered card at the top of the main panel.  
3. Show the current inequality slider value (rounded) with a qualitative label:
   - 0.0–0.2 → “low”  
   - 0.2–0.5 → “medium”  
   - 0.5–1.0 → “high”  

This card should appear **above** the charts and update whenever the user changes state, inequality, or programs-per-CZ.

---

## 3. Visualization 2 – Local vs State Earnings Distribution

### Purpose

Help users understand what “within-state inequality” actually does. Show the **distribution of local high-school earnings** in the selected state and how they relate to the **single statewide benchmark**.

### Design

A simple horizontal **histogram or density plot** of `local_hs_earnings` for all CZs in the selected state, with a **vertical line** for the statewide HS median.

Label the chart clearly:

- Title: “Distribution of Local High-School Earnings (CZs in STATE)”  
- X-axis: “Local HS earnings ($)”  
- Vertical line: “Statewide HS median benchmark”

### Implementation Notes for Codex

1. After generating CZ-level synthetic data, build a small DataFrame with one row per CZ:
   - Columns needed: `cz_id`, `local_hs_earnings`, `state_hs_earnings`.  
2. Use a Plotly figure:
   - Histogram or density plot on `local_hs_earnings`.  
   - Add a vertical line at `state_hs_earnings` for the selected state.  
3. Place this chart **right below** the summary card and **above** the main scatter/bar charts.  
4. Include a short explanatory caption under the chart, e.g.:

> “Bars show the simulated local high-school earnings across commuting zones. The vertical line shows the single statewide benchmark used in current accountability rules.”

This will make the inequality slider’s effect directly visible (the histogram spreads out more or less as the slider moves).

---

## 4. Visualization 3 – Early vs Later Earnings Comparison (Sample Programs)

### Purpose

Give users a feel for the **time horizon** variable by showing how program earnings can change between early and later career points, and how that interacts with the benchmark.

This is an **illustrative** chart using a handful of sample programs, not every program in the state.

### Design

A small multi-line or grouped bar chart showing:

- For 5–10 randomly chosen programs in the state:
  - Early-career earnings  
  - Later-career earnings  
  - (Optional) Local HS earnings as a reference line  

The point is to show that many programs are closer to the benchmark early on and pull away later.

### Implementation Notes for Codex

1. After generating program-level data, **sample** a small number of programs (e.g., 5–10) from the selected state:
   - Ensure variety in CZ types (urban/rural) if that variable exists.  
2. Build a mini DataFrame with:
   - `program_id` (or short label)  
   - `early_earnings`  
   - `late_earnings`  
   - `local_hs_earnings`  
3. Create a Plotly chart:
   - Either grouped bars (Early vs Later) for each program,  
   - Or lines with two points per program (x = time horizon; y = earnings).  
4. Add a horizontal line at `state_hs_earnings` or `local_hs_earnings` for each program.  
5. Place this chart **below** the main scatter/bar row, under a heading like “Example Program Trajectories.”

Add a caption:

> “These sample programs illustrate how earnings measured 3–4 years after college can differ from earnings 10 years after entry. Programs that appear marginal at the early horizon often move further above the benchmark later.”

---

## 5. Narrative Enhancements Tied to New Visuals

Update the **Summary Narrative** section to incorporate the new visuals:

1. After computing metrics, generate a short intro sentence like:

> “STATE currently has CZ_COUNT commuting zones with local high-school earnings ranging from $X to $Y around a statewide benchmark of $Z.”

2. Optionally, reference the histogram:

> “Under the current inequality setting, most local labor markets cluster below the statewide benchmark, which increases the chance that programs in those areas fail under a statewide rule even when they beat their local earnings bar.”

3. If possible, mention the early vs late comparison:

> “In these examples, several programs that are only slightly above the high-school benchmark at 3–4 years are substantially higher by 10 years.”

This ties the charts together into a coherent story for the user.

---

## 6. Placement Summary (Order of Elements in the Main Panel)

Codex should aim for this vertical order:

1. **Page title & short description** (already present)  
2. **State & Simulation Summary Card** (new)  
3. **Local vs State Earnings Distribution chart** (new)  
4. **Main row** (existing):
   - Left: benchmark distance scatterplot  
   - Right: pass/fail bar chart  
5. **Summary Narrative** (existing, enhanced)  
6. **Early vs Later Earnings sample chart** (new)  
7. **Raw Data Preview** expander (existing)

This ordering lets users first understand the state and its assumptions, then see the high-level misclassification patterns, and finally explore details.

---

## 7. Non-Goals for This Round

- No map-based visualizations yet.  
- No sector or demographic filtering.  
- No additional sidebar controls.  

The goal of these new visualizations is **interpretability**, not complexity.

---

**End of Additional Visualizations Specification**
