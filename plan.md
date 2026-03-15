# ep-analyzer: Implementation Plan

## Overview
A new standalone repo (`ep-analyzer`) with a **Next.js frontend** and **FastAPI backend**, using real data copied from `edu-accountability`. The app demonstrates how geographic bias in statewide earnings benchmarks misclassifies college programs, targeting policymakers and institutions.

## Architecture

```
ep-analyzer/
├── backend/                     # FastAPI
│   ├── app/
│   │   ├── main.py              # FastAPI app, CORS config
│   │   ├── routers/
│   │   │   ├── institutions.py  # Institution lookup, search, peer comparison
│   │   │   ├── states.py        # State-level risk distribution, thresholds
│   │   │   ├── analysis.py      # Reclassification, sensitivity, margin analysis
│   │   │   └── overview.py      # National summary stats
│   │   ├── data/
│   │   │   └── loader.py        # Parquet loading + caching
│   │   ├── models/
│   │   │   └── schemas.py       # Pydantic response models
│   │   └── services/
│   │       ├── benchmark.py     # Statewide vs local benchmark logic
│   │       └── risk.py          # Risk classification, margin calculations
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                    # Next.js (App Router)
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx       # Root layout, nav, footer
│   │   │   ├── page.tsx         # Landing / national overview
│   │   │   ├── states/
│   │   │   │   └── [state]/page.tsx  # State drill-down
│   │   │   ├── institutions/
│   │   │   │   ├── page.tsx          # Search/browse
│   │   │   │   └── [id]/page.tsx     # Institution detail
│   │   │   └── analysis/
│   │   │       └── page.tsx          # Reclassification + sensitivity
│   │   ├── components/
│   │   │   ├── charts/          # Recharts-based visualizations
│   │   │   │   ├── RiskDistribution.tsx
│   │   │   │   ├── MarginHistogram.tsx
│   │   │   │   ├── QuadrantScatter.tsx
│   │   │   │   ├── SectorBreakdown.tsx
│   │   │   │   └── EarningsComparison.tsx
│   │   │   ├── ui/              # Shared UI components (shadcn/ui)
│   │   │   ├── InstitutionCard.tsx
│   │   │   ├── StateSelector.tsx
│   │   │   └── SensitivitySlider.tsx
│   │   └── lib/
│   │       └── api.ts           # API client helpers
│   ├── package.json
│   └── Dockerfile
├── data/                        # Copied from edu-accountability
│   ├── ep_analysis.parquet
│   ├── program_counts.parquet
│   ├── scorecard_earnings.csv
│   └── state_thresholds_2024.csv
├── docker-compose.yml           # Local dev orchestration
├── README.md
└── .gitignore
```

## Data Files to Copy

From `edu-accountability`:
1. `data/processed/ep_analysis.parquet` (365 KB) — main dataset: 6,429 institutions with earnings, thresholds, risk levels, sector, enrollment, grad rates, program counts
2. `data/processed/program_counts.parquet` (54 KB) — program-level counts per institution
3. `data/raw/college_scorecard/scorecard_earnings.csv` (290 KB) — P6 + P10 earnings for early/late comparison
4. `data/raw/ep_thresholds/state_thresholds_2024.csv` (1 KB) — official state benchmarks

Total data: ~710 KB. No large files.

## Backend API Endpoints

### Overview
- `GET /api/overview` — National summary: total institutions, risk distribution counts, states covered

### States
- `GET /api/states` — All states with institution count, risk breakdown, threshold
- `GET /api/states/{state}` — State detail: institutions list, risk distribution, margin histogram data

### Institutions
- `GET /api/institutions?search=&state=&sector=&risk=` — Search/filter with pagination
- `GET /api/institutions/{unit_id}` — Single institution: earnings, margin, risk, peers
- `GET /api/institutions/{unit_id}/peers` — Same-state, same-sector peers ranked by margin

### Analysis
- `GET /api/analysis/reclassification?state=&inequality=` — Statewide vs synthetic-local benchmark comparison. Generates local CZ earnings using the same parametric model from ep_sim, but anchored to real state thresholds. Returns 4-quadrant classification.
- `GET /api/analysis/sensitivity?unit_id=&earnings_change=` — "What if earnings dropped by X%?" for a specific institution
- `GET /api/analysis/margins?state=&sector=` — Margin distribution data for histogram (how close to the cliff)
- `GET /api/analysis/early-vs-late?state=` — P6 vs P10 earnings comparison

## Frontend Pages

### 1. Landing Page (`/`)
- Hero: "X institutions serving Y students face earnings premium risk"
- National risk distribution donut chart
- Top-level stats: institutions by risk level, sector breakdown
- "Explore by state" grid/map

### 2. State View (`/states/[state]`)
- State threshold displayed prominently
- Risk distribution bar chart for that state
- Margin histogram: how far above/below the threshold each institution falls
- Sector breakdown within state
- Table of institutions sortable by margin, enrollment, sector

### 3. Institution Lookup (`/institutions`)
- Search by name with autocomplete
- Filter sidebar: state, sector, risk level
- Results as cards showing key metrics
- Click through to detail page

### 4. Institution Detail (`/institutions/[id]`)
- Institution card: name, state, sector, enrollment, grad rate
- Earnings vs threshold gauge/bar visualization
- Margin and risk classification
- P6 vs P10 earnings comparison (early vs late)
- Peer comparison table (same state + sector)
- Program count info (total, assessable, completions)

### 5. Analysis Page (`/analysis`)
- **Reclassification tool**: Select a state, adjust inequality slider → see the 4-quadrant scatter (pass-state vs pass-local) using real institutions from that state with synthetic local variation
- **Sensitivity explorer**: Select institution, drag slider to simulate earnings changes → see when it crosses the threshold
- **Margin distribution**: National or by-state histogram of earnings margins, highlighting the "danger zone" (0-20% above threshold)
- **Sector equity view**: Risk levels broken down by sector, with enrollment weights

## Implementation Steps

### Phase 1: Project Setup
1. Create `ep-analyzer/` repo structure
2. Initialize Next.js app with TypeScript, Tailwind, shadcn/ui
3. Initialize FastAPI backend with uvicorn
4. Copy data files from edu-accountability
5. Set up docker-compose for local dev
6. Configure CORS, basic health check endpoint

### Phase 2: Backend — Data Layer + Core APIs
7. Build parquet loader with caching (load once at startup)
8. Implement Pydantic response models
9. Build `/api/overview` endpoint
10. Build `/api/states` and `/api/states/{state}` endpoints
11. Build `/api/institutions` search/filter endpoint
12. Build `/api/institutions/{unit_id}` detail endpoint

### Phase 3: Frontend — Core Pages
13. Root layout with navigation (shadcn/ui)
14. Landing page with national overview stats + risk donut chart
15. State view page with risk distribution + margin histogram
16. Institution search page with filters
17. Institution detail page with earnings gauge + peer comparison

### Phase 4: Backend — Analysis Endpoints
18. Port ep_sim's benchmark reclassification logic (geo.py + evaluation.py) into `services/benchmark.py`
19. Build `/api/analysis/reclassification` endpoint
20. Build `/api/analysis/sensitivity` endpoint
21. Build `/api/analysis/margins` endpoint
22. Build `/api/analysis/early-vs-late` endpoint

### Phase 5: Frontend — Analysis Page
23. Reclassification tool with quadrant scatter chart
24. Sensitivity slider with threshold crossing visualization
25. Margin distribution histogram
26. Sector equity breakdown chart

### Phase 6: Polish + Deploy
27. Responsive design pass
28. Loading states, error handling
29. README with setup instructions
30. Docker compose verified end-to-end
