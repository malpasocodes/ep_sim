"""Phase 4: Synthetic program generation logic."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence

import numpy as np

from . import config, geo


@dataclass(frozen=True)
class Program:
    """Represents a synthetic program located within a commuting zone."""

    program_id: str
    program_type: str
    cz_id: str
    state_code: str
    cz_type: str
    local_hs_earnings: float
    early_earnings: float
    late_earnings: float

    @property
    def earnings_by_horizon(self) -> dict[str, float]:
        return {"early": self.early_earnings, "late": self.late_earnings}


def _draw_program_type(rng: np.random.Generator) -> str:
    types = list(config.PROGRAM_TYPE_WEIGHTS.keys())
    weights = list(config.PROGRAM_TYPE_WEIGHTS.values())
    return rng.choice(types, p=weights)


def _draw_bump(
    rng: np.random.Generator,
    *,
    program_type: str,
    horizon_key: str,
) -> float:
    low, high = config.PROGRAM_BUMP_RANGES[program_type][horizon_key]
    return rng.uniform(low, high)


def _calc_program_earnings(
    base_local_hs: float,
    rng: np.random.Generator,
    *,
    program_type: str,
) -> tuple[float, float]:
    early_bump = _draw_bump(rng, program_type=program_type, horizon_key="early")
    late_bump = _draw_bump(rng, program_type=program_type, horizon_key="late")
    early_noise = rng.normal(0, 1_000)
    late_noise = rng.normal(0, 1_500)
    early = base_local_hs * (1 + early_bump) + early_noise
    late = base_local_hs * (1 + late_bump) + late_noise
    return round(early, 2), round(late, 2)


def generate_programs(
    states: Sequence[geo.State],
    *,
    programs_per_cz: int | None = None,
    seed: int | None = None,
) -> List[Program]:
    """Generate synthetic programs for all commuting zones."""

    per_cz = programs_per_cz or config.DEFAULT_PROGRAMS_PER_CZ
    rng = np.random.default_rng(seed)
    programs: List[Program] = []

    for state in states:
        for cz in state.commuting_zones:
            for index in range(per_cz):
                program_type = _draw_program_type(rng)
                early, late = _calc_program_earnings(
                    cz.local_hs_earnings,
                    rng,
                    program_type=program_type,
                )
                program_id = f"{cz.cz_id}-{index:03d}"
                programs.append(
                    Program(
                        program_id=program_id,
                        program_type=program_type,
                        cz_id=cz.cz_id,
                        state_code=state.code,
                        cz_type=cz.cz_type,
                        local_hs_earnings=cz.local_hs_earnings,
                        early_earnings=early,
                        late_earnings=late,
                    )
                )

    return programs


def programs_to_records(programs: Iterable[Program]) -> list[dict]:
    """Flatten program dataclasses into simple dicts for pandas ingestion."""

    return [
        {
            "program_id": prog.program_id,
            "program_type": prog.program_type,
            "cz_id": prog.cz_id,
            "cz_type": prog.cz_type,
            "state_code": prog.state_code,
            "local_hs_earnings": prog.local_hs_earnings,
            "early_earnings": prog.early_earnings,
            "late_earnings": prog.late_earnings,
        }
        for prog in programs
    ]


__all__ = ["Program", "generate_programs", "programs_to_records"]
