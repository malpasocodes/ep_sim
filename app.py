"""Streamlit entry point for the Earnings Premium Simulation tool."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from simulation import config, evaluation, geo, programs, visuals

DATA_PATH = Path("data/commuting_zones.csv")


@st.cache_data(show_spinner=False)
def load_states(inequality_level: float, seed: int | None) -> dict[str, geo.State]:
    return geo.build_states(DATA_PATH, inequality_level=inequality_level, seed=seed)


@st.cache_data(show_spinner=False)
def generate_programs_cache(
    state_map: dict[str, geo.State],
    programs_per_cz: int,
    seed: int | None,
):
    return programs.generate_programs(list(state_map.values()), programs_per_cz=programs_per_cz, seed=seed)


def render_sidebar() -> dict:
    st.sidebar.header("Simulation Controls")
    seed = st.sidebar.number_input("Random Seed", min_value=0, value=42, step=1)
    selected_state = st.sidebar.selectbox(
        "State",
        options=["All"] + sorted(config.STATE_HS_EARNINGS.keys()),
        index=0,
    )
    horizon_key = st.sidebar.radio(
        "Time Horizon",
        options=["early", "late"],
        format_func=lambda key: config.TIME_HORIZONS[key].label,
        horizontal=False,
    )
    inequality = st.sidebar.slider(
        "Within-State Inequality",
        min_value=0.0,
        max_value=1.0,
        value=config.DEFAULT_INEQUALITY_LEVEL,
    )
    programs_per_cz = st.sidebar.slider(
        "Programs per CZ",
        min_value=5,
        max_value=80,
        value=config.DEFAULT_PROGRAMS_PER_CZ,
        step=5,
    )
    return {
        "seed": seed,
        "state": selected_state,
        "horizon": horizon_key,
        "inequality": inequality,
        "programs_per_cz": programs_per_cz,
    }


def filter_programs(program_list: list[programs.Program], state_code: str) -> list[programs.Program]:
    if state_code == "All":
        return program_list
    return [prog for prog in program_list if prog.state_code == state_code]


def main() -> None:
    st.set_page_config(page_title="Earnings Premium Simulation", layout="wide")
    st.title("Earnings Premium Simulation")
    st.write(
        "Explore how statewide vs. local high-school earnings benchmarks affect pass/fail outcomes "
        "for synthetic college programs across commuting zones."
    )

    controls = render_sidebar()
    states_map = load_states(controls["inequality"], controls["seed"])
    program_list = generate_programs_cache(
        states_map,
        controls["programs_per_cz"],
        controls["seed"],
    )
    filtered_programs = filter_programs(program_list, controls["state"])

    df = evaluation.evaluate_programs(filtered_programs, horizon=controls["horizon"])
    summary = evaluation.summarize_classifications(df)

    col1, col2 = st.columns((2, 1))
    with col1:
        st.plotly_chart(visuals.scatter_distance_plot(df), use_container_width=True)
    with col2:
        st.plotly_chart(visuals.classification_bar(summary), use_container_width=True)

    st.subheader("Summary Narrative")
    st.write(visuals.generate_narrative(summary))

    with st.expander("Raw Data Preview"):
        st.dataframe(df.head(50))


if __name__ == "__main__":
    main()
