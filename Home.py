import streamlit as st
from utils import load_data, inject_base_style, page_header, LATEST_POP_COL

st.set_page_config(
    page_title="World Population Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_base_style()
df = load_data()

page_header(
    "🌍", "World Population Analysis Dashboard",
    "Explore global population trends, growth, and density — 1970 to 2026.",
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Countries / Territories", f"{df.shape[0]:,}")
col2.metric("Total Population (2026)", f"{df[LATEST_POP_COL].sum():,.0f}")
col3.metric("Continents Covered", df["Continent"].nunique())
col4.metric(
    "Top Country",
    df.loc[df[LATEST_POP_COL].idxmax(), "Country/Territory"],
)

st.markdown("")
st.markdown(
    """
    ### 👋 Welcome

    This dashboard is split across three pages, available from the sidebar:

    - **📈 Visualization** — interactive charts: top countries, continent share,
      population trends over time, density, and correlations.
    - **📊 Statistical Report** — descriptive statistics, dataset quality checks,
      and a continent-by-continent breakdown.
    - **💡 Key Insights** — the headline numbers and fastest/slowest movers at a glance.

    Use the **Continent** and **Country** filters in the sidebar on any page to
    narrow the data — they carry the same behavior across the whole app.
    """
)

st.divider()
with st.expander("📄 Preview the raw dataset"):
    st.dataframe(df, use_container_width=True, height=350)

st.caption(
    "Built with Streamlit, Pandas, and Plotly. "
    "Swap in your own `data/wp.csv` (same columns) to use real data."
)
