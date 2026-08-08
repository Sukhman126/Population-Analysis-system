"""Shared helpers used across every page of the dashboard."""
from pathlib import Path
import pandas as pd
import streamlit as st

DATA_PATH = Path(__file__).resolve().parent / "data" / "wp.csv"

YEAR_COLUMNS = [
    "1970 Population", "1980 Population", "1990 Population", "2000 Population",
    "2010 Population", "2015 Population", "2020 Population", "2022 Population",
    "2023 Population", "2024 Population", "2025 Population", "2026 Population",
]
YEARS = [1970, 1980, 1990, 2000, 2010, 2015, 2020, 2022, 2023, 2024, 2025, 2026]

# Single source of truth for "the latest year" — update this one line (and
# regenerate/refresh the dataset) to roll the whole app forward next year.
LATEST_YEAR = 2026
LATEST_POP_COL = f"{LATEST_YEAR} Population"


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load the population dataset once and cache it for every page."""
    if not DATA_PATH.exists():
        st.error(
            f"Couldn't find the dataset at `{DATA_PATH}`. "
            "Make sure `wp.csv` is inside the `data/` folder."
        )
        st.stop()
    df = pd.read_csv(DATA_PATH)
    df.columns = [c.strip() for c in df.columns]
    return df


def inject_base_style():
    """A little shared CSS so every page feels like one product, not three scripts."""
    st.markdown(
        """
        <style>
        .block-container {padding-top: 2rem; padding-bottom: 3rem;}
        [data-testid="stMetric"] {
            background: rgba(120, 120, 255, 0.06);
            border: 1px solid rgba(120, 120, 255, 0.15);
            border-radius: 12px;
            padding: 14px 16px 10px 16px;
        }
        [data-testid="stMetricLabel"] {font-weight: 600;}
        h1, h2, h3 {font-weight: 700;}
        .tagline {color: var(--text-color-secondary, #8a8a8a); margin-top: -8px;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(icon: str, title: str, subtitle: str = ""):
    st.title(f"{icon} {title}")
    if subtitle:
        st.markdown(f"<p class='tagline'>{subtitle}</p>", unsafe_allow_html=True)
    st.divider()


def sidebar_filters(df: pd.DataFrame):
    """Consistent continent/country filters, reused on every page. Returns filtered df."""
    st.sidebar.header("🔎 Filters")

    continents = ["All"] + sorted(df["Continent"].dropna().unique().tolist())
    selected_continent = st.sidebar.selectbox("Continent", continents)
    if selected_continent != "All":
        df = df[df["Continent"] == selected_continent]

    countries = ["All"] + sorted(df["Country/Territory"].dropna().unique().tolist())
    selected_country = st.sidebar.selectbox("Country / Territory", countries)
    if selected_country != "All":
        df = df[df["Country/Territory"] == selected_country]

    st.sidebar.markdown("---")
    st.sidebar.caption(f"Showing **{df.shape[0]}** rows × **{df.shape[1]}** columns")

    return df
