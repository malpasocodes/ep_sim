"""Phase 6: Plotly visualization helpers for the simulation outputs."""

from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


CLASSIFICATION_COLORS = {
    "Pass Both": "#1b9e77",
    "Pass Local Only": "#d95f02",
    "Pass State Only": "#7570b3",
    "Fail Both": "#e7298a",
}


def scatter_distance_plot(df: pd.DataFrame) -> go.Figure:
    """Quadrant scatterplot: local distance (x) vs state distance (y)."""

    fig = px.scatter(
        df,
        x="distance_local",
        y="distance_state",
        color="classification",
        color_discrete_map=CLASSIFICATION_COLORS,
        hover_data={
            "program_id": True,
            "program_type": True,
            "state_code": True,
            "cz_type": True,
            "local_benchmark": ":,.0f",
            "state_benchmark": ":,.0f",
            "earnings": ":,.0f",
            "distance_local": ":,.0f",
            "distance_state": ":,.0f",
        },
        labels={
            "distance_local": "Earnings – Local HS benchmark ($)",
            "distance_state": "Earnings – State HS benchmark ($)",
            "classification": "Pass/Fail Category",
        },
    )
    fig.update_layout(
        title="Benchmark Distance Comparison",
        legend_title="Classification",
        template="plotly_white",
        xaxis=dict(zeroline=True, zerolinecolor="#999999"),
        yaxis=dict(zeroline=True, zerolinecolor="#999999"),
    )
    return fig


def classification_bar(summary_df: pd.DataFrame) -> go.Figure:
    """Bar chart showing counts per classification category."""

    summary_df = summary_df.sort_values("classification")
    fig = px.bar(
        summary_df,
        x="classification",
        y="count",
        color="classification",
        color_discrete_map=CLASSIFICATION_COLORS,
        text=summary_df["share"].map(lambda x: f"{x:.0%}"),
        labels={"classification": "Category", "count": "Programs"},
    )
    fig.update_layout(
        title="Pass/Fail Mix",
        template="plotly_white",
        showlegend=False,
    )
    return fig


def local_earnings_distribution(
    cz_df: pd.DataFrame,
    *,
    state_label: str,
    state_benchmark: float,
) -> go.Figure:
    """Histogram showing distribution of local HS earnings with statewide median line."""

    fig = px.histogram(
        cz_df,
        x="local_hs_earnings",
        nbins=20,
        labels={"local_hs_earnings": "Local HS earnings ($)"},
        title=f"Distribution of Local High-School Earnings – {state_label}",
    )
    fig.add_vline(
        x=state_benchmark,
        line_dash="dash",
        line_color="#333333",
        annotation_text="Statewide benchmark",
        annotation_position="top right",
    )
    fig.update_layout(template="plotly_white")
    return fig


def sample_program_earnings_chart(
    sample_df: pd.DataFrame,
    *,
    state_benchmark: float | None = None,
) -> go.Figure:
    """Grouped bar chart comparing early vs late earnings for sample programs."""

    melted = sample_df.melt(
        id_vars=["program_id"],
        value_vars=["early_earnings", "late_earnings"],
        var_name="horizon",
        value_name="earnings",
    )
    horizon_labels = {
        "early_earnings": "Early (3–4 yrs)",
        "late_earnings": "Later (10 yrs)",
    }
    melted["horizon"] = melted["horizon"].map(horizon_labels)

    fig = px.bar(
        melted,
        x="program_id",
        y="earnings",
        color="horizon",
        barmode="group",
        labels={"program_id": "Program", "earnings": "Earnings ($)", "horizon": "Time Horizon"},
        title="Sample Program Trajectories",
    )
    if state_benchmark:
        fig.add_hline(
            y=state_benchmark,
            line_dash="dash",
            line_color="#333333",
            annotation_text="Statewide benchmark",
            annotation_position="top left",
        )
    fig.update_layout(template="plotly_white")
    return fig


def generate_narrative(
    summary_df: pd.DataFrame,
    *,
    state_label: str,
    cz_count: int,
    cz_min: float,
    cz_max: float,
    state_benchmark: float | None,
    horizon_label: str,
    inequality_label: str,
) -> str:
    """Produce narrative text linking the visuals together."""

    total = summary_df["count"].sum()
    if total == 0:
        return "No programs generated for the selected inputs."

    top = summary_df.sort_values("share", ascending=False).iloc[0]
    share = f"{top['share']:.0%}"
    base = (
        f"{state_label} currently includes {cz_count} synthetic commuting zones with local high-school earnings "
        f"spanning ${cz_min:,.0f} to ${cz_max:,.0f}"
    )
    if state_benchmark:
        base += f" around a statewide benchmark of ${state_benchmark:,.0f}"
    base += (
        f'. Under the {horizon_label.lower()} horizon ({inequality_label} inequality), {share} of simulated programs fall into '
        f'the “{top["classification"]}” group.'
    )
    return base


__all__ = [
    "scatter_distance_plot",
    "classification_bar",
    "local_earnings_distribution",
    "sample_program_earnings_chart",
    "generate_narrative",
    "CLASSIFICATION_COLORS",
]
