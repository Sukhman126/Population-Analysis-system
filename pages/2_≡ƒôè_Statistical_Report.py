import streamlit as st
import plotly.express as px

from utils import load_data, inject_base_style, page_header, sidebar_filters, LATEST_POP_COL

st.set_page_config(page_title="Statistical Report", page_icon="📊", layout="wide")
inject_base_style()

df_full = load_data()
df = sidebar_filters(df_full)

page_header("📊", "Statistical Report", "Descriptive statistics and data-quality checks.")

if df.empty:
    st.warning("No rows match the current filters. Try widening your selection in the sidebar.")
    st.stop()

# ---------------- Dataset overview ---------------- #
st.header("📁 Dataset Overview")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Countries", df.shape[0])
c2.metric("Total Features", df.shape[1])
c3.metric("Missing Values", int(df.isnull().sum().sum()))
c4.metric("Duplicate Records", int(df.duplicated().sum()))
st.divider()

# ---------------- Descriptive statistics ---------------- #
st.header("📈 Descriptive Statistics")
st.dataframe(df.describe(), use_container_width=True)
st.divider()

# ---------------- Population statistics ---------------- #
st.header("🌍 Population Statistics")

highest = df.loc[df[LATEST_POP_COL].idxmax()]
lowest = df.loc[df[LATEST_POP_COL].idxmin()]
average = df[LATEST_POP_COL].mean()
median = df[LATEST_POP_COL].median()
std = df[LATEST_POP_COL].std()

c1, c2, c3 = st.columns(3)
c1.metric("Average Population", f"{average:,.0f}")
c2.metric("Median Population", f"{median:,.0f}")
c3.metric("Standard Deviation", f"{std:,.0f}")

col1, col2 = st.columns(2)
with col1:
    st.write("#### 🏆 Highest Population Country")
    st.success(
        f"**{highest['Country/Territory']}** ({highest['Continent']})\n\n"
        f"Population: **{highest[LATEST_POP_COL]:,}**"
    )
with col2:
    st.write("#### 📉 Lowest Population Country")
    st.info(
        f"**{lowest['Country/Territory']}** ({lowest['Continent']})\n\n"
        f"Population: **{lowest[LATEST_POP_COL]:,}**"
    )
st.divider()

# ---------------- Top / Bottom 10 ---------------- #
col1, col2 = st.columns(2)
with col1:
    st.header("🏆 Top 10 Most Populated")
    top10 = df.nlargest(10, LATEST_POP_COL)[["Country/Territory", "Continent", LATEST_POP_COL]]
    st.dataframe(top10, use_container_width=True, hide_index=True)
with col2:
    st.header("📉 Bottom 10 Least Populated")
    bottom10 = df.nsmallest(10, LATEST_POP_COL)[["Country/Territory", "Continent", LATEST_POP_COL]]
    st.dataframe(bottom10, use_container_width=True, hide_index=True)
st.divider()

# ---------------- Continent summary ---------------- #
st.header("🌎 Continent-wise Population")
continent = (
    df.groupby("Continent")[LATEST_POP_COL]
    .sum()
    .sort_values(ascending=False)
)
c1, c2 = st.columns([1, 2])
with c1:
    st.dataframe(continent, use_container_width=True)
with c2:
    st.bar_chart(continent)
st.divider()

# ---------------- Density statistics ---------------- #
st.header("🏙 Population Density Statistics")
st.dataframe(df["Density (per km²)"].describe().to_frame(), use_container_width=True)
st.divider()

# ---------------- Missing values ---------------- #
st.header("🔍 Missing Values")
missing = df.isnull().sum()
missing = missing[missing > 0]
if missing.empty:
    st.success("✅ No missing values found in the dataset.")
else:
    st.dataframe(missing.to_frame(name="Missing Values"), use_container_width=True)
st.divider()

# ---------------- Correlation matrix ---------------- #
st.header("📌 Correlation Matrix")
numeric_df = df.select_dtypes(include="number")
corr = numeric_df.corr()
fig = px.imshow(
    corr, text_auto=".2f", aspect="auto",
    color_continuous_scale="RdBu_r", zmin=-1, zmax=1,
)
st.plotly_chart(fig, use_container_width=True)
st.divider()

# ---------------- Key insights ---------------- #
st.header("📋 Key Insights")
st.markdown(
    f"""
- 🌍 Total countries in view: **{df.shape[0]}**
- 🏆 Highest population country: **{highest['Country/Territory']}**
- 📉 Lowest population country: **{lowest['Country/Territory']}**
- 📊 Average population: **{average:,.0f}**
- 🌎 Continents represented: **{df['Continent'].nunique()}**
- 📈 Population data spans **1970–2022**
"""
)

st.success("Statistical report generated successfully ✅")
