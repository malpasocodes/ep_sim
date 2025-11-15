# Product Requirements Document (PRD)
## Earnings Premium Simulation – Version 1

### 1. Overview
#### 1.1 Product Name  
Earnings Premium Simulation Tool (Version 1)

#### 1.2 Version  
v1 – Synthetic Data Prototype

#### 1.3 Document Purpose  
This document defines the requirements, scope, and objectives for Version 1 of the Earnings Premium Simulation Tool. It provides guidance for development, UI/UX design, and deployment.

#### 1.4 Summary of the Product  
The Earnings Premium Simulation Tool demonstrates how different earnings benchmarks—statewide vs. local—produce different pass/fail outcomes under a college accountability framework. Version 1 uses synthetic data with realistic assumptions to illustrate these effects across all U.S. states and their commuting zones.

#### 1.5 Alignment with EDU Accountability Lab Mission  
The tool advances the Lab’s mission of providing independent, data-driven insights into college accountability and outcomes by revealing structural biases embedded in current policy metrics.

---

### 2. Problem Statement
#### 2.1 What Problem Are We Solving?  
Current federal accountability measures rely on **statewide high-school earnings** as the benchmark for evaluating college programs. This benchmark does not reflect the actual labor markets in which students live and work.

#### 2.2 Why This Matters  
Using a single statewide number introduces statistical flaws, misclassifying many programs—especially those in lower-wage or rural regions. These misclassifications can have high-stakes consequences.

#### 2.3 Evidence-Based Motivation  
Research shows large within-state variation in earnings, strong local labor-market ties among graduates, and structural differences between early and late career earnings. These contextual factors motivate the need for a simulation that visualizes the effects.

---

### 3. Goals & Objectives
#### 3.1 Primary Goals  
- Demonstrate the sensitivity of pass/fail outcomes to benchmark choice.  
- Provide policymakers with an intuitive way to understand geographic bias.  
- Build a foundation for later versions using real data.

#### 3.2 Secondary Goals  
- Allow comparison across early vs. later time horizons.  
- Serve as an educational tool for presentations and briefings.

#### 3.3 Non-Goals  
- Version 1 will not use real institutional earnings or demographics.  
- It will not attempt to model fields of study or student-level outcomes.

#### 3.4 Success Metrics  
- Users can easily toggle state/local benchmarks and observe differences.  
- Output clearly communicates misclassification patterns.  
- Performance remains smooth with synthetic data.

---

### 4. Users & Use Cases
#### 4.1 Primary Users  
Policymakers, legislative staff, think tanks, journalists, higher-education researchers.

#### 4.2 Secondary Users  
Institutional leaders, students, advocacy organizations.

#### 4.3 Core Use Cases  
- Demonstrating flaws in statewide accountability metrics.  
- Exploring how geography affects outcomes.  
- Understanding early vs. late earnings effects.

#### 4.4 Pain Points Addressed  
Users lack intuitive tools that show how measurement choices distort accountability outcomes.

---

### 5. Product Description
#### 5.1 High-Level Concept  
An interactive simulation that models how programs in different labor markets perform under statewide vs. local earnings benchmarks.

#### 5.2 Key Features  
- Synthetic U.S. map of states and commuting zones.  
- Sliders controlling within-state inequality.  
- Toggle for time horizon (3–4 years vs. 10 years).  
- Visual pass/fail comparison chart.

#### 5.3 Core Models  
- Statewide benchmark = state-level HS median earnings.  
- Local benchmark = CZ-level HS median earnings.  
- Program earnings = local HS earnings + program bump.

#### 5.4 Simulation Inputs  
Statewide earnings, local earnings, time horizon, inequality level.

#### 5.5 Simulation Outputs  
Pass/fail classifications, distribution of misclassified programs, visualizations.

#### 5.6 Assumptions  
All institutions synthetic; earnings bumps stylized; commuting zones real.

---

### 6. Functional Requirements
#### 6.1 Simulation Logic  
- Generate synthetic programs per CZ.  
- Compute earnings premium under both benchmarks.  
- Classify program outcomes.

#### 6.2 UI Requirements  
- Clean Streamlit interface with sidebar controls.  
- Two-column layout with controls on left, charts on right.

#### 6.3 Data Requirements  
- Synthetic data only; commuting zone list from Census crosswalk.

#### 6.4 Visualization Requirements  
- Plotly scatterplot (local vs state distance).  
- Summary tables for classification.

#### 6.5 Performance Requirements  
- All operations compute under 1 second.

#### 6.6 Logging  
Optional basic logs for debugging.

---

### 7. Non-Functional Requirements
Usability: intuitive to non-technical users  
Accessibility: readable on desktop and tablet  
Reliability: consistent results for same inputs  
Maintainability: modular codebase  
Extensibility: real data can replace synthetic inputs later

---

### 8. Technical Constraints
- Must run on Streamlit  
- Deployed on Render  
- Python environment only  
- Browser use only; no mobile-specific version required  
- No sensitive data processed

---

### 9. Risks & Mitigations
- Risk: Misinterpretation of synthetic results  
  Mitigation: Clear labeling and disclaimers  
- Risk: Overcomplication  
  Mitigation: Minimal variables in v1  
- Risk: Performance on Render  
  Mitigation: Lightweight simulation

---

### 10. Versioning & Future Enhancements
#### 10.1 Planned Versions  
- v1 Synthetic  
- v2 Real geography + partial real data  
- v3 Full institutional data

#### 10.2 Extensions  
Institutional sector, demographics, field of study.

#### 10.3 Long-Term Vision  
Integration with broader EDU Accountability Lab analytics platform.
