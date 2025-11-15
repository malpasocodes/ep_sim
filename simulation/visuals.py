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


def generate_narrative(summary_df: pd.DataFrame) -> str:
    """Produce a simple narrative sentence about classification shares."""

    total = summary_df["count"].sum()
    if total == 0:
        return "No programs generated for the selected inputs."

    top = summary_df.sort_values("share", ascending=False).iloc[0]
    category = top["classification"]
    share = f"{top['share']:.0%}"
    return f"{share} of simulated programs fall into the “{category}” bucket under the current settings."


__all__ = [
    "scatter_distance_plot",
    "classification_bar",
    "generate_narrative",
    "CLASSIFICATION_COLORS",
]
