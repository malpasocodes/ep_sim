# How to Interpret the Earnings Premium Simulation

Version 1 uses synthetic data to illustrate how statewide versus local high-school earnings benchmarks can misclassify college programs. Use this guide as a companion to the Streamlit app.

## 1. Understand the Inputs
- **State selector**: chooses which state’s commuting zones (CZs) are simulated. Large states have more CZs per the proportional mapping.
- **Time horizon**: early (3–4 years) vs. later (10 years) earnings snapshots. Later horizons typically show stronger earnings gains.
- **Within-state inequality slider**: controls the spread between local HS earnings and the statewide benchmark. Higher settings create wider disparities.
- **Programs per CZ**: total simulated programs = CZ count × slider value.

## 2. Read the Overview Section
- The **summary card** reports CZ count, programs per CZ, total programs, and the inequality setting (low/medium/high).
- The **local earnings histogram** shows the distribution of CZ-level HS earnings with a dashed line at the statewide median. If most bars fall below that line, programs in those labor markets are structurally disadvantaged by a statewide rule.

## 3. Interpret the Main Charts
- **Scatterplot** (local vs. state benchmark distances) places each program in a quadrant:
  - Upper-right: passes both benchmarks.
  - Lower-left: fails both.
  - Upper-left: passes statewide only.
  - Lower-right: passes local only (often the largest group in low-wage regions).
- **Bar chart** summarizes the share of programs in each pass/fail category. Large orange (“Pass Local Only”) bars highlight misclassification risk when using statewide metrics.

## 4. Narrative & Sample Programs
- The narrative now references CZ ranges, inequality setting, and the dominant classification share.
- The **sample program trajectories** compare early vs. later earnings for a handful of programs and overlay the statewide benchmark. Rising later-career bars show why longer horizons matter.

## 5. Talking Points for Policymakers
- Emphasize how many CZs lie below the statewide benchmark even when they meet local standards.
- Highlight programs that pass locally but fail statewide despite positive later-career trajectories.
- Use inequality slider adjustments to demonstrate sensitivity: small changes can flip many programs from fail to pass when local benchmarks are allowed.
