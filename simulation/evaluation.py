"""Phase 5: Benchmark comparison + classification logic."""

from __future__ import annotations

from dataclasses import asdict
from typing import Dict, Iterable, List, Mapping, Sequence

import pandas as pd

from . import config, programs

CLASSIFICATION_LABELS = {
    (True, True): "Pass Both",
    (True, False): "Pass State Only",
    (False, True): "Pass Local Only",
    (False, False): "Fail Both",
}


def _resolve_horizon_key(horizon: str | config.TimeHorizon) -> str:
    if isinstance(horizon, config.TimeHorizon):
        return horizon.key
    if horizon not in config.TIME_HORIZONS:
        raise ValueError(f"Unknown horizon '{horizon}'")
    return horizon


def _classify(program_earnings: float, state_benchmark: float, local_benchmark: float) -> str:
    state_pass = program_earnings >= state_benchmark
    local_pass = program_earnings >= local_benchmark
    return CLASSIFICATION_LABELS[(state_pass, local_pass)]


def evaluate_programs(
    program_list: Sequence[programs.Program],
    *,
    horizon: str | config.TimeHorizon,
    state_benchmarks: Mapping[str, int] | None = None,
) -> pd.DataFrame:
    """Return a DataFrame with pass/fail flags, distances, and classifications."""

    horizon_key = _resolve_horizon_key(horizon)
    state_lookup = state_benchmarks or config.STATE_HS_EARNINGS
    records: List[Dict] = []

    for prog in program_list:
        earnings = prog.earnings_by_horizon[horizon_key]
        state_benchmark = state_lookup[prog.state_code]
        local_benchmark = prog.local_hs_earnings
        state_pass = earnings >= state_benchmark
        local_pass = earnings >= local_benchmark
        classification = CLASSIFICATION_LABELS[(state_pass, local_pass)]

        records.append(
            {
                "program_id": prog.program_id,
                "state_code": prog.state_code,
                "cz_id": prog.cz_id,
                "cz_type": prog.cz_type,
                "program_type": prog.program_type,
                "earnings": earnings,
                "state_benchmark": state_benchmark,
                "local_benchmark": local_benchmark,
                "distance_state": round(earnings - state_benchmark, 2),
                "distance_local": round(earnings - local_benchmark, 2),
                "pass_state": state_pass,
                "pass_local": local_pass,
                "classification": classification,
                "horizon": horizon_key,
            }
        )

    return pd.DataFrame.from_records(records)


def summarize_classifications(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate classification counts + shares for UI bar charts."""

    counts = df["classification"].value_counts().rename_axis("classification").reset_index(name="count")
    total = counts["count"].sum()
    counts["share"] = counts["count"] / total if total else 0
    return counts


__all__ = ["evaluate_programs", "summarize_classifications"]
