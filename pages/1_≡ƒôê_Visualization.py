import streamlit as st
import pandas as pd
import plotly.express as px

from utils import load_data, inject_base_style, page_header, sidebar_filters, YEARS, YEAR_COLUMNS, LATEST_POP_COL

st.set_page_config(page_title="Visualization", page_icon="📈", layout="wide")
inject_base_style()

df_full = load_data()
df = sidebar_filters(df_full)

page_header("📈", "Visualization", "Interactive charts for exploring the dataset.")

if df.empty:
    st.warning("No rows match the current filters. Try widening your selection in the sidebar.")
    st.stop()

# ---------------- KPI row ---------------- #
c1, c2, c3, c4 = st.columns(4)
c1.metric("Countries", df["Country/Territory"].nunique())
c2.metric("Total Population", f"{df[LATEST_POP_COL].sum():,.0f}")
c3.metric("Avg Growth Rate", f"{df['Growth Rate'].mean():.4f}")
c4.metric("Avg Density (per km²)", f"{df['Density (per km²)'].mean():,.1f}")

st.divider()

# ---------------- Top 10 bar chart ---------------- #
st.subheader("🏆 Top 10 Countries by Population")
top10 = df.sort_values(LATEST_POP_COL, ascending=False).head(10)
fig = px.bar(
    top10, x="Country/Territory", y=LATEST_POP_COL,
    color=LATEST_POP_COL, color_continuous_scale="Blues",
    text_auto=".2s",
)
fig.update_layout(showlegend=False, xaxis_title="", yaxis_title=LATEST_POP_COL)
st.plotly_chart(fig, use_container_width=True)

# ---------------- Continent pie ---------------- #
st.subheader("🌎 Population Share by Continent")
continent = df.groupby("Continent")[LATEST_POP_COL].sum().reset_index()
fig = px.pie(continent, names="Continent", values=LATEST_POP_COL, hole=0.45)
fig.update_traces(textinfo="percent+label")
st.plotly_chart(fig, use_container_width=True)

# ---------------- Population trend for a selected country ---------------- #
st.subheader("📉 Population Trend Over Time")
country = st.selectbox("Select a country", sorted(df["Country/Territory"].unique()))
row = df[df["Country/Territory"] == country].iloc[0]
trend = pd.DataFrame({"Year": YEARS, "Population": [row[c] for c in YEAR_COLUMNS]})
fig = px.line(trend, x="Year", y="Population", markers=True)
fig.update_layout(yaxis_title="Population")
st.plotly_chart(fig, use_container_width=True)

# ---------------- Top 5 trend comparison (area chart) ---------------- #
st.subheader("📊 Top 5 Countries — Population Trend Comparison")
top5 = df.sort_values(LATEST_POP_COL, ascending=False).head(5)
long_rows = []
for _, r in top5.iterrows():
    for y, c in zip(YEARS, YEAR_COLUMNS):
        long_rows.append({"Country": r["Country/Territory"], "Year": y, "Population": r[c]})
trend5 = pd.DataFrame(long_rows)
fig = px.area(trend5, x="Year", y="Population", color="Country", groupnorm=None)
st.plotly_chart(fig, use_container_width=True)

# ---------------- Growth rate histogram ---------------- #
st.subheader("📶 Growth Rate Distribution")
fig = px.histogram(df, x="Growth Rate", nbins=25, color_discrete_sequence=["#2E8B57"])
st.plotly_chart(fig, use_container_width=True)

# ---------------- Scatter: area vs population ---------------- #
st.subheader("🗺️ Area vs. Population")
fig = px.scatter(
    df, x="Area (km²)", y=LATEST_POP_COL, color="Continent",
    size="Density (per km²)", hover_name="Country/Territory",
    size_max=40, log_x=True, log_y=True,
)
st.plotly_chart(fig, use_container_width=True)

# ---------------- Box plot: density by continent ---------------- #
st.subheader("🏙️ Population Density by Continent")
fig = px.box(df, x="Continent", y="Density (per km²)", color="Continent", points="all")
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# ---------------- Treemap ---------------- #
st.subheader("🌳 Treemap — Continent → Country")
fig = px.treemap(
    df, path=["Continent", "Country/Territory"], values=LATEST_POP_COL,
    color="Growth Rate", color_continuous_scale="RdYlGn_r",
)
st.plotly_chart(fig, use_container_width=True)

st.caption("Tip: use the sidebar filters to focus this whole page on one continent or country.")
