import streamlit as st

from utils import load_data, inject_base_style, page_header, sidebar_filters, LATEST_POP_COL

st.set_page_config(page_title="Key Insights", page_icon="💡", layout="wide")
inject_base_style()

df_full = load_data()
df = sidebar_filters(df_full)

page_header("💡", "Key Insights", "The headline numbers, at a glance.")

if df.empty:
    st.warning("No rows match the current filters. Try widening your selection in the sidebar.")
    st.stop()

# ---------------- KPIs ---------------- #
total_countries = df.shape[0]
total_population = df[LATEST_POP_COL].sum()
largest_country = df.loc[df[LATEST_POP_COL].idxmax(), "Country/Territory"]
smallest_country = df.loc[df[LATEST_POP_COL].idxmin(), "Country/Territory"]
avg_growth = df["Growth Rate"].mean()

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("🌍 Countries", total_countries)
c2.metric("👨‍👩‍👧‍👦 Total Population", f"{total_population:,.0f}")
c3.metric("📈 Avg Growth Rate", f"{avg_growth:.4f}")
c4.metric("🏆 Highest Population", largest_country)
c5.metric("📉 Lowest Population", smallest_country)

st.divider()

# ---------------- Insight cards ---------------- #
c1, c2 = st.columns(2)

with c1:
    st.success(
        f"### 🌎 Largest Population\n\n"
        f"**{largest_country}**\n\n"
        f"Population (2026): **{df[LATEST_POP_COL].max():,}**"
    )
    fastest = df.loc[df["Growth Rate"].idxmax()]
    st.warning(
        f"### 🚀 Fastest Growing\n\n"
        f"**{fastest['Country/Territory']}**\n\n"
        f"Growth Rate: **{fastest['Growth Rate']}**"
    )

with c2:
    st.info(
        f"### 🌍 Smallest Population\n\n"
        f"**{smallest_country}**\n\n"
        f"Population (2026): **{df[LATEST_POP_COL].min():,}**"
    )
    slowest = df.loc[df["Growth Rate"].idxmin()]
    st.error(
        f"### 🐢 Slowest Growing\n\n"
        f"**{slowest['Country/Territory']}**\n\n"
        f"Growth Rate: **{slowest['Growth Rate']}**"
    )

st.divider()

# ---------------- Top 5 by population, as progress bars ---------------- #
st.subheader("🏅 Top 5 Most Populated Countries")
top5 = df.nlargest(5, LATEST_POP_COL)[["Country/Territory", LATEST_POP_COL]]
max_pop = top5[LATEST_POP_COL].max()
for _, row in top5.iterrows():
    st.write(f"**{row['Country/Territory']}**")
    st.progress(float(row[LATEST_POP_COL] / max_pop))
    st.caption(f"{row[LATEST_POP_COL]:,}")

st.divider()

# ---------------- Fun facts ---------------- #
st.subheader("📌 Interesting Facts")
st.markdown(
    f"""
✅ This view contains **{total_countries} countries and territories**

✅ Combined 2022 population is **{total_population:,.0f}**

✅ Highest population country is **{largest_country}**

✅ Lowest population country is **{smallest_country}**

✅ Average growth rate is **{avg_growth:.4f}**

✅ Population data ranges from **1970 to 2022**
"""
)

st.success(
    "🎯 These insights help identify population distribution, growth trends, "
    "and global demographic patterns at a glance."
)

st.divider()

# ---------------- About the project ---------------- #
with st.expander("📖 About this project"):
    st.write(
        """
        **World Population Analysis Dashboard** is an interactive data-visualization
        app built with Python and Streamlit. It analyzes population statistics for
        countries around the world and surfaces trends in growth, density, and
        continent-wise distribution through interactive charts.

        **Built with:** Python · Streamlit · Pandas · Plotly
        """
    )
