import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="KEMU SACCO Financial Dashboard", layout="wide")
st.title("📊 KEMU SACCO Financial Dashboard")
st.markdown("### Statement of Comprehensive Income Analysis (2021–2025)")

# ---------- DATA (extracted from audited reports) ----------
@st.cache_data
def load_data():
    data = {
        "Year": [2021, 2022, 2023, 2024, 2025],
        "Interest on member loans": [7_008_550, 10_040_602, 15_519_495, 16_061_859, 13_614_392],
        "Other interest income": [34_007, 555_957, 244_135, 124_143, 108_247],
        "Divided income (dividends)": [1_347_754, 1_154_586, 1_610_642, 1_654_482, 2_736_857],
        "Fees & commissions (net)": [64_770, 72_360, 69_500, 61_500, 66_500],
        "MPESA & trading income": [46_950, 119_289, 169_599, 214_660, 155_413],
        "Total Revenue": [8_623_839, 12_060_719, 17_628_373, 18_116_644, 16_681_409],
        "Salaries & wages": [1_605_804, 1_495_742, 1_609_176, 1_639_465, 1_736_883],
        "Provision for loan losses": [0, 339_961, 905_839, 1_039_725, 563_637],
        "Interest expense (external)": [104_200, 359_467, 111_318, 283_343, 876_717],
        "Governance costs (meetings + travel + education)": [788_780, 983_042, 1_109_738, 1_296_087, 1_924_700],
        "Other operating expenses": [1_382_265, 1_413_990, 981_844, 1_273_493, 1_211_216],
        "Total Expenditure": [3_881_049, 4_592_202, 4_717_915, 5_531_113, 6_313_153],
        "Surplus before interest on deposits": [4_742_790, 7_468_516, 12_910_458, 12_585_531, 10_368_256],
        "Interest on member deposits (cost of funds)": [2_902_848, 4_660_475, 5_623_754, 7_026_676, 7_343_068],
        "Net Surplus before tax": [1_839_942, 2_808_041, 7_286_704, 5_558_855, 3_025_188],
        "Taxation": [3_716, 4_789, 36_620, 18_621, 16_237],
        "Net Surplus after tax": [1_836_226, 2_803_252, 7_250_084, 5_540_234, 3_008_951],
        "Proposed Dividends": [1_109_573, 1_692_624, 2_439_542, 2_556_428, 2_862_288],
        "Retained Earnings (after dividends)": [159_408, 149_978, 4_810_542, 2_983_806, 146_663],
    }
    df = pd.DataFrame(data)
    # Calculate key ratios
    df["Cost of funds / Revenue (%)"] = (df["Interest on member deposits (cost of funds)"] / df["Total Revenue"]) * 100
    df["Net surplus margin (%)"] = (df["Net Surplus after tax"] / df["Total Revenue"]) * 100
    df["Dividend payout ratio (%)"] = (df["Proposed Dividends"] / df["Net Surplus after tax"]) * 100
    return df

df = load_data()

# ---------- SIDEBAR FILTERS ----------
st.sidebar.header("Filters")
years = st.sidebar.multiselect("Select Years", df["Year"].unique(), default=df["Year"].unique())
if not years:
    years = df["Year"].unique()
filtered_df = df[df["Year"].isin(years)]

# ---------- KEY METRICS (Latest Year) ----------
latest = df[df["Year"] == df["Year"].max()].iloc[0]
col1, col2, col3, col4 = st.columns(4)
col1.metric("📈 Total Revenue (2025)", f"Ksh {latest['Total Revenue']:,.0f}", 
            delta=f"{((latest['Total Revenue']/df[df['Year']==2024]['Total Revenue'].values[0])-1)*100:.1f}%")
col2.metric("💰 Net Surplus after tax", f"Ksh {latest['Net Surplus after tax']:,.0f}",
            delta=f"{((latest['Net Surplus after tax']/df[df['Year']==2024]['Net Surplus after tax'].values[0])-1)*100:.1f}%")
col3.metric("💸 Proposed Dividends", f"Ksh {latest['Proposed Dividends']:,.0f}",
            delta=f"{((latest['Proposed Dividends']/df[df['Year']==2024]['Proposed Dividends'].values[0])-1)*100:.1f}%")
col4.metric("🏦 Retained Earnings", f"Ksh {latest['Retained Earnings (after dividends)']:,.0f}",
            delta=f"{latest['Retained Earnings (after dividends)'] - df[df['Year']==2024]['Retained Earnings (after dividends)'].values[0]:,.0f}")

st.markdown("---")

# ---------- PLOT 1: REVENUE VS EXPENSES ----------
st.subheader("📊 Revenue vs Total Expenditure (2021–2025)")
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=filtered_df["Year"], y=filtered_df["Total Revenue"], mode="lines+markers", name="Total Revenue", line=dict(color="green")))
fig1.add_trace(go.Scatter(x=filtered_df["Year"], y=filtered_df["Total Expenditure"], mode="lines+markers", name="Total Expenditure", line=dict(color="red")))
fig1.update_layout(xaxis_title="Year", yaxis_title="Amount (Ksh)", hovermode="x unified")
st.plotly_chart(fig1, use_container_width=True)

# ---------- PLOT 2: NET SURPLUS & DIVIDENDS ----------
st.subheader("💰 Net Surplus after tax vs Proposed Dividends")
fig2 = go.Figure()
fig2.add_trace(go.Bar(x=filtered_df["Year"], y=filtered_df["Net Surplus after tax"], name="Net Surplus after tax", marker_color="teal"))
fig2.add_trace(go.Scatter(x=filtered_df["Year"], y=filtered_df["Proposed Dividends"], name="Proposed Dividends", mode="lines+markers", line=dict(color="orange", width=3)))
fig2.update_layout(xaxis_title="Year", yaxis_title="Amount (Ksh)")
st.plotly_chart(fig2, use_container_width=True)

# ---------- PLOT 3: KEY RATIOS ----------
st.subheader("📐 Key Financial Ratios (%)")
ratio_cols = ["Cost of funds / Revenue (%)", "Net surplus margin (%)", "Dividend payout ratio (%)"]
fig3 = px.line(filtered_df, x="Year", y=ratio_cols, markers=True, labels={"value": "Percentage (%)", "variable": "Ratio"})
st.plotly_chart(fig3, use_container_width=True)

# ---------- PLOT 4: REVENUE COMPOSITION (STACKED AREA) ----------
st.subheader("📌 Revenue Composition")
revenue_components = ["Interest on member loans", "Other interest income", "Divided income (dividends)", 
                      "Fees & commissions (net)", "MPESA & trading income"]
fig4 = px.area(filtered_df, x="Year", y=revenue_components, title="Revenue Breakdown by Source", 
               labels={"value": "Ksh", "variable": "Revenue Source"})
st.plotly_chart(fig4, use_container_width=True)

# ---------- PLOT 5: EXPENSE TRENDS ----------
st.subheader("📉 Major Expense Categories")
expense_cols = ["Salaries & wages", "Provision for loan losses", "Interest expense (external)", "Governance costs (meetings + travel + education)"]
fig5 = px.line(filtered_df, x="Year", y=expense_cols, markers=True, labels={"value": "Ksh", "variable": "Expense Type"})
st.plotly_chart(fig5, use_container_width=True)

# ---------- DATA TABLE ----------
st.subheader("📋 Full Data Table (2021–2025)")
st.dataframe(filtered_df.style.format("{:,.0f}", subset=[col for col in filtered_df.columns if filtered_df[col].dtype in ['int64', 'float64']]), use_container_width=True)

# ---------- DOWNLOAD BUTTON ----------
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button("⬇️ Download filtered data as CSV", data=csv, file_name="kemu_sacco_data.csv", mime="text/csv")
