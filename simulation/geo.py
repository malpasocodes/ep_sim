"""Phase 3: Synthetic state + commuting zone scaffolding."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Sequence

import numpy as np

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
    *,
    inequality_level: float,
    seed: int | None = None,
) -> Dict[str, State]:
    """Create a dictionary of states keyed by state code."""

    rng = np.random.default_rng(seed)
    states: Dict[str, State] = {}
    cz_types = list(config.CZ_TYPE_SHARES.keys())
    cz_weights = list(config.CZ_TYPE_SHARES.values())

    for code, state_hs in config.STATE_HS_EARNINGS.items():
        state_name = config.STATE_NAMES.get(code, code)
        cz_count = config.get_state_cz_count(code)
        state = State(code=code, name=state_name, state_hs_earnings=state_hs)

        for idx in range(cz_count):
            cz_type = rng.choice(cz_types, p=cz_weights)
            cz_id = f"{code}-{idx+1:03d}"
            cz_name = f"{state_name} CZ {idx+1}"
            local_hs = _assign_local_earnings(
                state_hs,
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

        states[code] = state

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
]
