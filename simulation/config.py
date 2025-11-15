"""Configuration constants and helper utilities for the synthetic simulation.

Phase 2 centralizes core parameters so later phases (CZ generation, program
generation, evaluation, UI) can pull from a single source of truth.
"""

from __future__ import annotations

from dataclasses import dataclass
import csv
import logging
from pathlib import Path
from typing import Dict, Tuple

# ---------------------------------------------------------------------------
# Time horizons (early vs. late career) definitions
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TimeHorizon:
    """Metadata describing an earnings measurement window."""

    key: str
    label: str
    years_after_grad: Tuple[int, int]
    description: str


TIME_HORIZONS: Dict[str, TimeHorizon] = {
    "early": TimeHorizon(
        key="early",
        label="Early career",
        years_after_grad=(3, 4),
        description="Roughly 3–4 years after completion (aligned with SSA data windows).",
    ),
    "late": TimeHorizon(
        key="late",
        label="Later career",
        years_after_grad=(10, 10),
        description="A decade after entry, capturing longer-run labor market attachment.",
    ),
}

# ---------------------------------------------------------------------------
# Earnings bump multipliers by program type + horizon
# Values represent additive percentages applied to local HS earnings.
# ---------------------------------------------------------------------------

PROGRAM_TYPES = ("two_year", "four_year")

PROGRAM_BUMP_RANGES: Dict[str, Dict[str, Tuple[float, float]]] = {
    "two_year": {
        "early": (0.04, 0.08),
        "late": (0.07, 0.12),
    },
    "four_year": {
        "early": (0.06, 0.12),
        "late": (0.10, 0.18),
    },
}

# ---------------------------------------------------------------------------
# Inequality slider configuration
# The UI slider will emit a value between 0 and 1. We map that to a standard
# deviation (in dollars) for local HS earnings offsets relative to the state.
# ---------------------------------------------------------------------------

MIN_INEQUALITY_STD = 1_500  # slider == 0
MAX_INEQUALITY_STD = 8_000  # slider == 1
DEFAULT_INEQUALITY_LEVEL = 0.35  # mid-low skew


def inequality_std(slider_value: float) -> float:
    """Map a 0-1 slider value to a dollar STD for CZ earnings spreads."""

    bounded = max(0.0, min(1.0, slider_value))
    return MIN_INEQUALITY_STD + (MAX_INEQUALITY_STD - MIN_INEQUALITY_STD) * bounded


# ---------------------------------------------------------------------------
# Statewide HS earnings (synthetic) – baseline medians by state.
# Values are stylized but preserve intuitive ordering across regions.
# ---------------------------------------------------------------------------

STATE_HS_EARNINGS: Dict[str, int] = {
    "AL": 31000,
    "AK": 42000,
    "AZ": 33500,
    "AR": 30000,
    "CA": 42500,
    "CO": 41000,
    "CT": 45500,
    "DE": 39500,
    "DC": 48000,
    "FL": 33000,
    "GA": 34000,
    "HI": 41000,
    "ID": 32000,
    "IL": 38500,
    "IN": 34500,
    "IA": 35000,
    "KS": 34500,
    "KY": 31500,
    "LA": 30500,
    "ME": 36000,
    "MD": 44000,
    "MA": 46500,
    "MI": 35500,
    "MN": 38000,
    "MS": 29000,
    "MO": 33500,
    "MT": 33000,
    "NE": 35000,
    "NV": 34000,
    "NH": 39500,
    "NJ": 45500,
    "NM": 30500,
    "NY": 43000,
    "NC": 33000,
    "ND": 36000,
    "OH": 35000,
    "OK": 31500,
    "OR": 37000,
    "PA": 38000,
    "RI": 40000,
    "SC": 32000,
    "SD": 33500,
    "TN": 33000,
    "TX": 35000,
    "UT": 36000,
    "VT": 36500,
    "VA": 40500,
    "WA": 41500,
    "WV": 30000,
    "WI": 35000,
    "WY": 36000,
}

STATE_NAMES: Dict[str, str] = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "DC": "District of Columbia",
    "FL": "Florida",
    "GA": "Georgia",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PA": "Pennsylvania",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming",
}

_LOGGER = logging.getLogger(__name__)
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
STATE_CZ_MAPPING_PATH = DATA_DIR / "state_cz_mapping.csv"
DEFAULT_CZ_COUNT = 8


def _load_state_cz_mapping() -> Dict[str, int]:
    mapping: Dict[str, int] = {}
    if not STATE_CZ_MAPPING_PATH.exists():  # pragma: no cover - dev safeguard
        _LOGGER.warning("state_cz_mapping.csv missing at %s", STATE_CZ_MAPPING_PATH)
        return mapping
    with STATE_CZ_MAPPING_PATH.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            try:
                code = row["state"].strip().upper()
                mapping[code] = int(row["cz_count"])
            except (KeyError, ValueError):
                continue
    return mapping


STATE_CZ_COUNTS = _load_state_cz_mapping()


def get_state_hs_earnings(state_code: str) -> int:
    """Return the statewide HS earnings benchmark for the provided state."""

    code = state_code.upper()
    try:
        return STATE_HS_EARNINGS[code]
    except KeyError as exc:  # pragma: no cover - defensive branch
        raise ValueError(f"Unknown state code: {state_code}") from exc


def get_state_cz_count(state_code: str) -> int:
    """Return the synthetic commuting zone count for a state."""

    code = state_code.upper()
    count = STATE_CZ_COUNTS.get(code)
    if count is None:
        _LOGGER.warning("Missing CZ count for %s, defaulting to %s", code, DEFAULT_CZ_COUNT)
        return DEFAULT_CZ_COUNT
    return count


# ---------------------------------------------------------------------------
# CZ type assumptions (used when generating local earnings draws)
# ---------------------------------------------------------------------------

CZ_TYPE_SHARES: Dict[str, float] = {
    "urban": 0.35,
    "suburban": 0.40,
    "rural": 0.25,
}

# For each CZ type, specify the multiplier bounds relative to the state median.
# Example: for an urban CZ we draw a multiplier between 0.9x and 1.25x.
CZ_LOCAL_EARNINGS_MULTIPLIERS: Dict[str, Tuple[float, float]] = {
    "urban": (0.90, 1.25),
    "suburban": (0.85, 1.10),
    "rural": (0.70, 1.00),
}

# ---------------------------------------------------------------------------
# Program generation defaults
# ---------------------------------------------------------------------------

DEFAULT_PROGRAMS_PER_CZ = 40
PROGRAM_TYPE_WEIGHTS: Dict[str, float] = {
    "two_year": 0.55,
    "four_year": 0.45,
}


@dataclass(frozen=True)
class SimulationDefaults:
    """Simple container bundling the most common knobs for convenience."""

    horizon: TimeHorizon
    inequality: float
    programs_per_cz: int


SIM_DEFAULTS = SimulationDefaults(
    horizon=TIME_HORIZONS["early"],
    inequality=DEFAULT_INEQUALITY_LEVEL,
    programs_per_cz=DEFAULT_PROGRAMS_PER_CZ,
)


__all__ = [
    "CZ_LOCAL_EARNINGS_MULTIPLIERS",
    "CZ_TYPE_SHARES",
    "DATA_DIR",
    "DEFAULT_CZ_COUNT",
    "DEFAULT_PROGRAMS_PER_CZ",
    "DEFAULT_INEQUALITY_LEVEL",
    "PROGRAM_BUMP_RANGES",
    "PROGRAM_TYPE_WEIGHTS",
    "PROGRAM_TYPES",
    "SIM_DEFAULTS",
    "STATE_HS_EARNINGS",
    "STATE_NAMES",
    "STATE_CZ_COUNTS",
    "STATE_CZ_MAPPING_PATH",
    "TIME_HORIZONS",
    "TimeHorizon",
    "get_state_hs_earnings",
    "get_state_cz_count",
    "inequality_std",
]
