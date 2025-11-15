# UI/UX Specification  
## Earnings Premium Simulation – Version 1  
### EDU Accountability Lab

---

## 1. Design Philosophy

The UI/UX design for Version 1 of the Earnings Premium Simulation Tool follows the visual and structural conventions already established in the EDU Accountability Lab’s Streamlit applications. The emphasis is on clarity, simplicity, and credibility. The interface must feel familiar to existing Lab users: clean side navigation, wide content panels, consistent spacing, and understated but polished design elements. The interface should make the simulation intuitive even for non-technical policymakers while maintaining enough depth to satisfy researchers.

The design must foreground interpretation rather than visual complexity. Every chart, table, and control should explicitly reinforce the central concept: statewide versus local benchmarks produce systematically different outcomes. The UX must reduce cognitive load, provide frictionless interactions, and guide the user toward key insights through narrative structure.

---

## 2. Overall Layout

The application follows a two-region structure: a persistent left sidebar for navigation and controls, and a main content area for explanations, charts, and results.

### Sidebar
The left sidebar houses:
- Page navigation (Streamlit multipage or custom radio menu)
- Simulation controls (state selector, time horizon toggle, inequality slider, number of programs)
- Optional advanced toggles (e.g., show only distressed areas)

### Main Panel
The center area includes:
1. A short explanatory header describing what the simulation does.
2. A clean, wide section displaying dynamic charts (Plotly).
3. A narrative block explaining the results in plain language.
4. A secondary visualization or summary table.

This matches the visual logic of the existing EDU Accountability Lab site and preserves continuity.

---

## 3. Navigation Structure

Navigation remains consistent with existing pages. Suggested structure:

- **Home**
- **College Value Grid**
- **Federal Loans**
- **Earnings Premium & ROI**
- **Earnings Premium Simulation** ← *New page*

The new page inherits the same visual markers (icons, section headers) for consistency.

---

## 4. Interaction Model

The user interacts with the simulation through a small number of well-chosen controls. Each control triggers immediate regeneration of the simulation results.

### Controls (Left Sidebar)
1. **State Selector**  
   Dropdown with all 50 states + DC. Default: “All States” or “Select a State.”

2. **Time Horizon**  
   Radio buttons:  
   - “Early career (3–4 years after college)”  
   - “Later career (10 years after entry)”

3. **Within-State Inequality Slider**  
   A continuous slider representing how far local earnings can deviate from statewide median.  
   Range: Low → High.

4. **Number of Programs**  
   Simple slider defining how many synthetic programs are simulated per state.  
   Default: moderate number (e.g., 50–100 programs per state).

5. **Optional: Highlight Distressed Labor Markets**  
   Checkbox to color-code CZs with below-state earnings.

### Interaction Principles
- No more than 4–5 primary controls to preserve simplicity.
- All interactions must produce near-instant feedback (<1s).
- Charts update immediately following any control change.
- The explanatory text updates dynamically based on results.

---

## 5. Visual Components

### 5.1 Header Section
A simple title (“Earnings Premium Simulation”) followed by one paragraph summarizing the purpose of the simulation. Tone: explanatory and accessible.

### 5.2 Primary Visualization (Plotly Scatter)
A quadrant scatterplot with:
- **X-axis:** Distance from local benchmark  
- **Y-axis:** Distance from statewide benchmark  
- Each point = a synthetic program  
- Color: program classification or CZ type  
- Tooltip: local HS earnings, program type, early/late earnings, pass/fail status

Quadrants visually represent:
- Pass both
- Fail both
- Pass local / fail state
- Pass state / fail local

This mirrors the visual logic of the report and grounds the statistical flaw in a simple picture.

### 5.3 Secondary Visualization (Bar Chart)
A bar chart showing:
- Number (or percentage) of programs in each classification
- Bars labeled clearly: “Pass Local Only,” “Pass State Only,” “Pass Both,” “Fail Both”

### 5.4 Summary Text Block
A narrative interpretation automatically generated from simulation results. For example:

> “In this simulation, 28% of programs located in distressed labor markets pass the local benchmark but fail the statewide benchmark. Programs in high-wage regions rarely fail either threshold.”

This ensures clarity for policymakers.

---

## 6. Content Structure

Each simulation page will have the following structure:

1. **Title + subtitle**  
2. **Short explanation (3–4 sentences)**  
3. **Simulation controls (sidebar)**  
4. **Primary chart**  
5. **Secondary chart or summary table**  
6. **Narrative interpretation**  
7. **Disclaimers** (e.g., “Synthetic data only, Version 1 prototype”)

---

## 7. Accessibility Considerations

- High-contrast colors for markers and axes.
- Legible font size (Streamlit default or slightly increased).
- Clear tooltips and alt-text equivalents.
- Keyboard navigation supported through Streamlit defaults.
- Avoid overly dense chart elements.

---

## 8. Mobile/Tablet Behavior

Streamlit is not optimized for mobile-first interaction, so Version 1 targets desktop and tablet screens.  
Ensure:
- Sidebar collapses gracefully.
- Charts scale without clipping.
- Horizontal scrolling is avoided.

---

## 9. Consistency with Existing EDU Accountability Lab Visual Identity

To maintain alignment with your current Streamlit deployment:
- Use the same font and default Streamlit theme (light).
- Follow the same spacing and alignment conventions.
- Preserve navigation structure, icons, and section headers.
- Use similar color palettes for charts where feasible.
- Keep explanatory text concise and neutral in tone.

---

## 10. Future UI/UX Enhancements (Version 2+)

Future versions may introduce:
- Real institution data overlays
- State maps showing CZ distributions
- Program-level filtering (sector, Pell share, MSI status)
- Multi-page deep dives per state

These are excluded from Version 1 but anticipated.

---

## **End of UI/UX Specification**
