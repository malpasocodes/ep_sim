"""Phase 3: Synthetic state + commuting zone scaffolding.

Reads the commuting-zone crosswalk and generates dataclass-backed objects with
local high-school earnings derived from the statewide benchmark and inequality
settings defined in ``simulation.config``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Sequence

import numpy as np
import pandas as pd

from . import config


@dataclass(frozen=True)
class CommutingZone:
    """Represents a commuting zone with assigned synthetic HS earnings."""

    cz_id: str
    name: str
    cz_type: str
    local_hs_earnings: float


@dataclass
class State:
    """Represents a state and its collection of commuting zones."""

    code: str
    name: str
    state_hs_earnings: int
    commuting_zones: List[CommutingZone] = field(default_factory=list)

    def add_cz(self, cz: CommutingZone) -> None:
        self.commuting_zones.append(cz)


class CrosswalkColumns:
    STATE_CODE = "state_code"
    STATE_NAME = "state_name"
    CZ_ID = "cz_id"
    CZ_NAME = "cz_name"
    CZ_TYPE = "cz_type"


REQUIRED_COLUMNS = (
    CrosswalkColumns.STATE_CODE,
    CrosswalkColumns.STATE_NAME,
    CrosswalkColumns.CZ_ID,
    CrosswalkColumns.CZ_NAME,
    CrosswalkColumns.CZ_TYPE,
)


def load_crosswalk(path: Path | str) -> pd.DataFrame:
    """Load and validate the commuting-zone crosswalk CSV."""

    df = pd.read_csv(path, dtype=str).dropna()
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:  # pragma: no cover - defensive guard for future edits
        raise ValueError(f"Crosswalk file missing columns: {missing}")
    return df


def _pick_multiplier(rng: np.random.Generator, cz_type: str) -> float:
    low, high = config.CZ_LOCAL_EARNINGS_MULTIPLIERS[cz_type]
    return rng.uniform(low, high)


def _assign_local_earnings(
    baseline: int,
    cz_type: str,
    inequality_level: float,
    rng: np.random.Generator,
) -> float:
    multiplier = _pick_multiplier(rng, cz_type)
    spread = config.inequality_std(inequality_level)
    noise = rng.normal(0.0, spread)
    earnings = baseline * multiplier + noise
    return max(20_000.0, round(earnings, 2))


def build_states(
    crosswalk_path: Path | str,
    *,
    inequality_level: float,
    seed: int | None = None,
) -> Dict[str, State]:
    """Create a dictionary of states keyed by state code."""

    df = load_crosswalk(crosswalk_path)
    rng = np.random.default_rng(seed)
    states: Dict[str, State] = {}

    for row in df.itertuples(index=False):
        code = getattr(row, CrosswalkColumns.STATE_CODE)
        name = getattr(row, CrosswalkColumns.STATE_NAME)
        cz_id = getattr(row, CrosswalkColumns.CZ_ID)
        cz_name = getattr(row, CrosswalkColumns.CZ_NAME)
        cz_type = getattr(row, CrosswalkColumns.CZ_TYPE).lower()

        if code not in config.STATE_HS_EARNINGS:
            raise ValueError(f"State {code} missing from STATE_HS_EARNINGS config")
        if cz_type not in config.CZ_LOCAL_EARNINGS_MULTIPLIERS:
            raise ValueError(f"CZ type '{cz_type}' missing multiplier config")

        state = states.setdefault(
            code,
            State(
                code=code,
                name=name,
                state_hs_earnings=config.STATE_HS_EARNINGS[code],
            ),
        )

        local_hs = _assign_local_earnings(
            state.state_hs_earnings,
            cz_type=cz_type,
            inequality_level=inequality_level,
            rng=rng,
        )
        state.add_cz(
            CommutingZone(
                cz_id=cz_id,
                name=cz_name,
                cz_type=cz_type,
                local_hs_earnings=local_hs,
            )
        )

    return states


def iter_commuting_zones(states: Sequence[State]) -> Iterable[CommutingZone]:
    """Convenience iterator to flatten all CZs across states."""

    for state in states:
        yield from state.commuting_zones


__all__ = [
    "CommutingZone",
    "State",
    "build_states",
    "iter_commuting_zones",
    "load_crosswalk",
]
