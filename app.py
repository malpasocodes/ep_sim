"""Streamlit entry point for the Earnings Premium Simulation tool."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from simulation import config, evaluation, geo, programs, visuals


@st.cache_data(show_spinner=False)
def load_states(inequality_level: float, seed: int | None) -> dict[str, geo.State]:
    return geo.build_states(inequality_level=inequality_level, seed=seed)


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


def select_states(state_map: dict[str, geo.State], state_code: str) -> list[geo.State]:
    if state_code == "All":
        return list(state_map.values())
    state = state_map.get(state_code)
    return [state] if state else []


def build_cz_dataframe(states_subset: list[geo.State]) -> pd.DataFrame:
    rows = []
    for state in states_subset:
        for cz in state.commuting_zones:
            rows.append(
                {
                    "state_code": state.code,
                    "state_name": state.name,
                    "cz_id": cz.cz_id,
                    "cz_type": cz.cz_type,
                    "local_hs_earnings": cz.local_hs_earnings,
                    "state_hs_earnings": state.state_hs_earnings,
                }
            )
    return pd.DataFrame(rows)


def describe_inequality(value: float) -> str:
    if value < 0.2:
        return "low"
    if value < 0.5:
        return "medium"
    return "high"


def build_program_sample_df(
    program_list: list[programs.Program],
    *,
    sample_size: int,
    seed: int,
) -> pd.DataFrame:
    if not program_list:
        return pd.DataFrame()
    program_df = pd.DataFrame(programs.programs_to_records(program_list))
    take = min(sample_size, len(program_df))
    return program_df.sample(n=take, random_state=seed)


def render_summary_card(
    *,
    state_label: str,
    cz_count: int,
    programs_per_cz: int,
    total_programs: int,
    inequality_value: float,
    inequality_desc: str,
) -> None:
    st.markdown(
        f"""
<div style="border:1px solid #e0e0e0; border-radius:8px; padding:1rem; margin-bottom:0.75rem;">
  <strong>State Overview: {state_label}</strong><br/>
  Commuting zones simulated: <strong>{cz_count:,}</strong><br/>
  Programs per CZ: <strong>{programs_per_cz}</strong><br/>
  Total programs: <strong>{total_programs:,}</strong><br/>
  Within-state inequality: <strong>{inequality_value:.2f} ({inequality_desc})</strong>
</div>
""",
        unsafe_allow_html=True,
    )


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
    selected_states = select_states(states_map, controls["state"])

    cz_df = build_cz_dataframe(selected_states)
    cz_count = len(cz_df)
    total_programs = len(filtered_programs)
    state_label = (
        "All States" if controls["state"] == "All" else config.STATE_NAMES.get(controls["state"], controls["state"])
    )
    state_benchmark = None if controls["state"] == "All" else config.get_state_hs_earnings(controls["state"])
    inequality_desc = describe_inequality(controls["inequality"])

    render_summary_card(
        state_label=state_label,
        cz_count=cz_count,
        programs_per_cz=controls["programs_per_cz"],
        total_programs=total_programs,
        inequality_value=controls["inequality"],
        inequality_desc=inequality_desc,
    )

    if controls["state"] == "All":
        st.info("Select a specific state to see how local high-school earnings compare with the statewide benchmark.")
    elif cz_df.empty:
        st.warning("No commuting zones generated for this state.")
    else:
        st.plotly_chart(
            visuals.local_earnings_distribution(
                cz_df,
                state_label=state_label,
                state_benchmark=state_benchmark,
            ),
            use_container_width=True,
        )
        st.caption(
            "Bars show simulated local high-school earnings across commuting zones; the dashed line is the statewide benchmark."
        )

    df = evaluation.evaluate_programs(filtered_programs, horizon=controls["horizon"])
    summary = evaluation.summarize_classifications(df)

    col1, col2 = st.columns((2, 1))
    with col1:
        st.plotly_chart(visuals.scatter_distance_plot(df), use_container_width=True)
    with col2:
        st.plotly_chart(visuals.classification_bar(summary), use_container_width=True)

    cz_min = float(cz_df["local_hs_earnings"].min()) if not cz_df.empty else 0.0
    cz_max = float(cz_df["local_hs_earnings"].max()) if not cz_df.empty else 0.0
    horizon_label = config.TIME_HORIZONS[controls["horizon"]].label

    st.subheader("Summary Narrative")
    st.write(
        visuals.generate_narrative(
            summary,
            state_label=state_label,
            cz_count=cz_count,
            cz_min=cz_min,
            cz_max=cz_max,
            state_benchmark=state_benchmark,
            horizon_label=horizon_label,
            inequality_label=inequality_desc,
        )
    )

    sample_df = build_program_sample_df(filtered_programs, sample_size=8, seed=controls["seed"])
    if controls["state"] == "All":
        st.info("Select a specific state to see example program trajectories by time horizon.")
    elif sample_df.empty:
        st.warning("No sample programs available for the selected filters.")
    else:
        st.subheader("Example Program Trajectories")
        st.plotly_chart(
            visuals.sample_program_earnings_chart(sample_df, state_benchmark=state_benchmark),
            use_container_width=True,
        )
        st.caption(
            "Sample programs illustrate how earnings measured 3–4 years after college can diverge further from the benchmark by year 10."
        )

    with st.expander("Raw Data Preview"):
        st.dataframe(df.head(50))


if __name__ == "__main__":
    main()
