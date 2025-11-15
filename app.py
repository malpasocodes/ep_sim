"""Streamlit entry point for the Earnings Premium Simulation tool."""

import streamlit as st


def main() -> None:
    st.set_page_config(page_title="Earnings Premium Simulation", layout="wide")
    st.title("Earnings Premium Simulation")
    st.write(
        "This placeholder app will eventually host the synthetic earnings premium "
        "simulation described in the project PRD."
    )
    st.info("Phase 1 placeholder – simulation and UI wiring land in later phases.")


if __name__ == "__main__":
    main()
