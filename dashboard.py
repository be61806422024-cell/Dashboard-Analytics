import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Financial Dashboard", layout="wide")
st.title("🏦 Financial Dashboard")
st.markdown("#### Statement of Comprehensive Income & Statement of Financial Position (2021–2025)")

# ------------------------------------------------------------
# DATA LOADING (Corrected figures from audited books)
# ------------------------------------------------------------
@st.cache_data
def load_income_data():
    """Income Statement data (P&L) 2021-2025"""
    data = {
        "Year": [2021, 2022, 2023, 2024, 2025],
        "Interest on member loans": [7_008_550, 10_040_602, 15_519_495, 16_061_859, 13_614_392],
        "Other operating income": [1_615_289, 2_020_117, 1_939_278, 1_840_125, 1_840_125],
        "Non-operating income": [0, 0, 169_599, 214_659, 214_659],
        "Total Revenue": [8_623_839, 12_060_719, 17_628_372, 18_116_644, 16_681_409],
        "Interest on member deposits": [2_902_848, 4_660_475, 6_739_653, 7_026_676, 7_343_068],
        "Personnel costs": [1_605_804, 1_495_742, 2_085_357, 2_085_357, 2_085_357],
        "Governance costs": [1_496_960, 1_670_040, 1_314_738, 1_453_062, 1_924_700],
        "Finance costs (excl deposit interest)": [203_459, 339_961, 1_185_816, 1_044_738, 563_637],
        "Administration expenses": [575_826, 730_280, 1_037_843, 948_956, 1_739_459],
        "Total Operating Costs": [3_881_049, 4_236_023, 5_623_754, 5_531_113, 6_313_153],
        "Net surplus before tax": [1_839_942, 2_808_042, 5_264_965, 5_558_855, 3_025_188],
        "Taxation": [3_716, 4_789, 36_620, 18_621, 16_237],
        "Net surplus after tax": [1_836_226, 2_803_253, 5_228_345, 5_540_234, 3_008_951],
        "Proposed Dividends": [1_109_573, 1_692_624, 2_439_542, 2_556_428, 2_862_288],
        "Retained Earnings (added to reserves)": [159_408, 149_978, 2_788_803, 2_983_806, 146_663],
    }
    df = pd.DataFrame(data)
    df["Cost of funds / Revenue (%)"] = (df["Interest on member deposits"] / df["Total Revenue"]) * 100
    df["Net surplus margin (%)"] = (df["Net surplus after tax"] / df["Total Revenue"]) * 100
    df["Dividend payout ratio (%)"] = (df["Proposed Dividends"] / df["Net surplus after tax"]) * 100
    return df

@st.cache_data
def load_balance_data():
    """Balance Sheet data 2021-2025 (aligned from user input)"""
    data = {
        "Year": [2021, 2022, 2023, 2024, 2025],
        "Cash and cash equivalents": [15_391_887, 10_003_073, 7_193_160, 4_330_722, 8_489_083],
        "Prepayments & sundry receivables": [16_844_094, 7_759_370, 2_683_771, 2_686_336, 12_092_018],
        "Inventories": [133_752, 129_378, 101_490, 93_468, 67_120],
        "Loans portfolio (net)": [49_204_037, 67_652_209, 89_338_126, 101_687_017, 109_878_332],
        "Financial investments": [3_955_265, 3_955_265, 4_055_050, 4_055_050, 4_055_050],
        "Intangible assets / Amortizable exp": [102_000, 0, 0, 0, 263_000],
        "Plant, property & equipment (net)": [487_452, 392_962, 305_703, 287_917, 335_203],
        "Total Assets": [86_118_487, 89_892_257, 103_677_300, 113_140_510, 135_179_806],
        "Interest on member deposits (accrued)": [3_183_592, 5_131_694, 7_297_736, 7_611_316, 8_034_094],
        "Proposed dividends payable": [1_628_623, 2_210_062, 3_013_947, 3_099_469, 3_509_189],
        "Non-withdrawable member deposits": [60_530_863, 64_310_597, 72_204_965, 75_149_058, 93_155_634],
        "Other member deposits": [6_177_913, 2_864_150, 1_868_876, 1_383_201, 0],
        "Insurance / RMF / RMP fund (net)": [-2_821_651, -3_168_238, -2_613_183, -2_094_208, -1_711_466],
        "Welfare fund": [63_600, 82_600, 0, 0, 0],
        "Payables and accruals": [502_281, 542_545, 283_761, 3_209_258, 6_263_678],
        "Total Liabilities": [69_265_221, 71_973_411, 82_056_102, 88_358_094, 109_251_129],
        "Share Capital": [11_095_728, 11_284_162, 12_197_711, 12_782_141, 14_311_440],
        "Reserves (statutory + revenue)": [5_757_540, 6_634_683, 9_423_486, 12_000_275, 11_617_238],
        "Total Shareholders' Funds": [16_853_268, 17_918_845, 21_621_197, 24_782_416, 25_928_678],
        "Total Liabilities & Equity": [86_118_488, 89_892_256, 103_677_299, 113_140_510, 135_179_807],
    }
    df = pd.DataFrame(data)
    df["Loans / Assets (%)"] = (df["Loans portfolio (net)"] / df["Total Assets"]) * 100
    df["Equity / Assets (%)"] = (df["Total Shareholders' Funds"] / df["Total Assets"]) * 100
    df["Cash / Assets (%)"] = (df["Cash and cash equivalents"] / df["Total Assets"]) * 100
    df["Member deposits / Assets (%)"] = (df["Non-withdrawable member deposits"] / df["Total Assets"]) * 100
    return df

# Load data
income_df = load_income_data()
balance_df = load_balance_data()

# Sidebar year selection
st.sidebar.header("Filters")
years_available = income_df["Year"].tolist()
selected_years = st.sidebar.multiselect("Select Years for Charts", years_available, default=years_available)
if not selected_years:
    selected_years = years_available

filtered_income = income_df[income_df["Year"].isin(selected_years)]
filtered_balance = balance_df[balance_df["Year"].isin(selected_years)]

# ------------------------------------------------------------
# Key Metrics Row with directional arrows (2025 vs 2024)
# ------------------------------------------------------------
st.header("📈 Key Metrics - Latest Year (2025)")

# Get 2025 and 2024 data
df_2025 = income_df[income_df["Year"] == 2025].iloc[0]
df_2024 = income_df[income_df["Year"] == 2024].iloc[0]
df_2021 = income_df[income_df["Year"] == 2021].iloc[0]
bal_2025 = balance_df[balance_df["Year"] == 2025].iloc[0]
bal_2024 = balance_df[balance_df["Year"] == 2024].iloc[0]

def format_delta_income(current, previous, reverse_color=False):
    delta = current - previous
    delta_percent = (delta / previous) * 100 if previous != 0 else 0
    if reverse_color:
        if delta > 0:
            return f"🔴 ▲ +{delta:,.0f} ({delta_percent:.1f}%)"
        elif delta < 0:
            return f"🟢 ▼ {delta:,.0f} ({delta_percent:.1f}%)"
        else:
            return "⚪ No change"
    else:
        if delta > 0:
            return f"🟢 ▲ +{delta:,.0f} ({delta_percent:.1f}%)"
        elif delta < 0:
            return f"🔴 ▼ {delta:,.0f} ({delta_percent:.1f}%)"
        else:
            return "⚪ No change"

def format_delta_balance(current, previous):
    delta = current - previous
    delta_percent = (delta / previous) * 100 if previous != 0 else 0
    if delta > 0:
        return f"🔵 ▲ +{delta:,.0f} ({delta_percent:.1f}%)"
    elif delta < 0:
        return f"🔵 ▼ {delta:,.0f} ({delta_percent:.1f}%)"
    else:
        return "⚪ No change"

# Compute year-on-year deltas (2025 vs 2024)
rev_delta = format_delta_income(df_2025["Total Revenue"], df_2024["Total Revenue"])
surplus_delta = format_delta_income(df_2025["Net surplus after tax"], df_2024["Net surplus after tax"])
expense_delta = format_delta_income(df_2025["Total Operating Costs"], df_2024["Total Operating Costs"], reverse_color=True)
assets_delta = format_delta_balance(bal_2025["Total Assets"], bal_2024["Total Assets"])
liabilities_delta = format_delta_balance(bal_2025["Total Liabilities"], bal_2024["Total Liabilities"])
equity_delta = format_delta_balance(bal_2025["Total Shareholders' Funds"], bal_2024["Total Shareholders' Funds"])

# Display 6 columns for year-on-year
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("💰 Total Revenue", f"Ksh {df_2025['Total Revenue']:,.0f}", delta=rev_delta)
col2.metric("📈 Net Surplus after tax", f"Ksh {df_2025['Net surplus after tax']:,.0f}", delta=surplus_delta)
col3.metric("⚠️ Total Operating Costs", f"Ksh {df_2025['Total Operating Costs']:,.0f}", delta=expense_delta)
col4.metric("🏛️ Total Assets", f"Ksh {bal_2025['Total Assets']:,.0f}", delta=assets_delta)
col5.metric("📜 Total Liabilities", f"Ksh {bal_2025['Total Liabilities']:,.0f}", delta=liabilities_delta)
col6.metric("👥 Shareholders' Funds", f"Ksh {bal_2025['Total Shareholders\' Funds']:,.0f}", delta=equity_delta)

# ------------------------------------------------------------
# CAGR (Compound Annual Growth Rate) over 5 years (2021–2025)
# ------------------------------------------------------------
st.subheader("📈 CAGR (2021–2025)")

def compute_cagr(start_val, end_val, years):
    if start_val <= 0:
        return None
    return (end_val / start_val) ** (1 / years) - 1

years = 4  # from 2021 to 2025 is 4 years of growth

rev_cagr = compute_cagr(df_2021["Total Revenue"], df_2025["Total Revenue"], years)
cost_cagr = compute_cagr(df_2021["Total Operating Costs"], df_2025["Total Operating Costs"], years)
surplus_cagr = compute_cagr(df_2021["Net surplus after tax"], df_2025["Net surplus after tax"], years)

def format_cagr(cagr_value, is_expense=False):
    if cagr_value is None:
        return "N/A"
    percent = cagr_value * 100
    if is_expense:
        if percent > 0:
            return f"🔴 ▲ +{percent:.1f}%"
        elif percent < 0:
            return f"🟢 ▼ {percent:.1f}%"
        else:
            return f"⚪ {percent:.1f}%"
    else:
        if percent > 0:
            return f"🟢 ▲ +{percent:.1f}%"
        elif percent < 0:
            return f"🔴 ▼ {percent:.1f}%"
        else:
            return f"⚪ {percent:.1f}%"

c1, c2, c3 = st.columns(3)
c1.metric("Total Revenue CAGR", format_cagr(rev_cagr), help="Compound Annual Growth Rate from 2021 to 2025")
c2.metric("Total Operating Costs CAGR", format_cagr(cost_cagr, is_expense=True), help="Compound Annual Growth Rate from 2021 to 2025")
c3.metric("Net Surplus after tax CAGR", format_cagr(surplus_cagr), help="Compound Annual Growth Rate from 2021 to 2025")

st.markdown("---")

# TABS
tab1, tab2 = st.tabs(["📊 Income Statement (P&L)", "🏛️ Balance Sheet (Statement of Financial Position)"])

# ================= TAB 1: INCOME STATEMENT =================
with tab1:
    st.subheader("💰 Income Statement Trends (2021–2025)")
    
    # Graph 1: Revenue vs Operating Costs
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=filtered_income["Year"], y=filtered_income["Total Revenue"], mode="lines+markers", name="Total Revenue"))
    fig1.add_trace(go.Scatter(x=filtered_income["Year"], y=filtered_income["Total Operating Costs"], mode="lines+markers", name="Operating Costs (excl deposit interest)"))
    fig1.update_layout(title="Revenue and Operating Costs", xaxis_title="Year", yaxis_title="Ksh")
    st.plotly_chart(fig1, use_container_width=True)
    
    # Graph 2: Operating Expenses Breakdown
    st.subheader("📉 Operating Expenses Breakdown (2021–2025)")
    expense_categories = ["Personnel costs", "Governance costs", "Finance costs (excl deposit interest)", "Administration expenses"]
    fig_expenses = px.line(filtered_income, x="Year", y=expense_categories, markers=True, title="Operating Expenses by Category")
    fig_expenses.update_layout(xaxis_title="Year", yaxis_title="Ksh")
    st.plotly_chart(fig_expenses, use_container_width=True)
    
    # Graph 3: Net Surplus vs Dividends
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=filtered_income["Year"], y=filtered_income["Net surplus after tax"], name="Net Surplus after tax"))
    fig2.add_trace(go.Scatter(x=filtered_income["Year"], y=filtered_income["Proposed Dividends"], name="Proposed Dividends", mode="lines+markers"))
    fig2.update_layout(title="Net Surplus vs Proposed Dividends", xaxis_title="Year", yaxis_title="Ksh")
    st.plotly_chart(fig2, use_container_width=True)
    
    # Graph 4: Key Ratios
    st.subheader("📐 Key Financial Ratios")
    ratio_df = filtered_income.melt(id_vars="Year", value_vars=["Cost of funds / Revenue (%)", "Net surplus margin (%)", "Dividend payout ratio (%)"])
    fig3 = px.line(ratio_df, x="Year", y="value", color="variable", markers=True, title="Ratios (%)")
    st.plotly_chart(fig3, use_container_width=True)
    
    # Data table
    with st.expander("📋 View Income Statement Data Table"):
        st.dataframe(filtered_income.style.format("{:,.0f}", subset=filtered_income.select_dtypes(include='number').columns))

# ================= TAB 2: BALANCE SHEET =================
with tab2:
    st.subheader("🏛️ Balance Sheet Trends (2021–2025)")
    
    # Total Assets, Liabilities, Equity
    fig_bal1 = go.Figure()
    fig_bal1.add_trace(go.Scatter(x=filtered_balance["Year"], y=filtered_balance["Total Assets"], mode="lines+markers", name="Total Assets"))
    fig_bal1.add_trace(go.Scatter(x=filtered_balance["Year"], y=filtered_balance["Total Liabilities"], mode="lines+markers", name="Total Liabilities"))
    fig_bal1.add_trace(go.Scatter(x=filtered_balance["Year"], y=filtered_balance["Total Shareholders' Funds"], mode="lines+markers", name="Shareholders' Funds"))
    fig_bal1.update_layout(title="Total Assets, Liabilities & Equity", xaxis_title="Year", yaxis_title="Ksh")
    st.plotly_chart(fig_bal1, use_container_width=True)
    
    # Major Asset Components
    st.subheader("📦 Major Asset Components")
    asset_components = ["Loans portfolio (net)", "Cash and cash equivalents", "Prepayments & sundry receivables", "Financial investments"]
    fig_assets = px.line(filtered_balance, x="Year", y=asset_components, markers=True, title="Asset Evolution")
    st.plotly_chart(fig_assets, use_container_width=True)
    
    # Major Liabilities
    st.subheader("📜 Major Liabilities")
    liability_components = ["Non-withdrawable member deposits", "Interest on member deposits (accrued)", "Proposed dividends payable", "Payables and accruals"]
    fig_liab = px.line(filtered_balance, x="Year", y=liability_components, markers=True, title="Liability Evolution")
    st.plotly_chart(fig_liab, use_container_width=True)
    
    # Equity Components
    st.subheader("👥 Shareholders' Equity")
    equity_components = ["Share Capital", "Reserves (statutory + revenue)"]
    fig_equity = px.line(filtered_balance, x="Year", y=equity_components, markers=True, title="Share Capital vs Reserves")
    st.plotly_chart(fig_equity, use_container_width=True)
    
    # Balance Sheet Ratios
    st.subheader("📊 Key Balance Sheet Ratios")
    ratio_bal_cols = ["Loans / Assets (%)", "Equity / Assets (%)", "Cash / Assets (%)", "Member deposits / Assets (%)"]
    ratio_bal_df = filtered_balance.melt(id_vars="Year", value_vars=ratio_bal_cols)
    fig_ratios_bal = px.line(ratio_bal_df, x="Year", y="value", color="variable", markers=True, title="Balance Sheet Ratios (%)")
    st.plotly_chart(fig_ratios_bal, use_container_width=True)
    
    # Data table
    with st.expander("📋 View Balance Sheet Data Table"):
        display_cols = [col for col in filtered_balance.columns if filtered_balance[col].dtype in ['int64', 'float64']]
        st.dataframe(filtered_balance.style.format("{:,.0f}", subset=display_cols))

# ------------------------------------------------------------
# DOWNLOAD BUTTONS (Sidebar)
# ------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("Download Data (CSV)")
csv_income = filtered_income.to_csv(index=False).encode('utf-8')
csv_balance = filtered_balance.to_csv(index=False).encode('utf-8')
st.sidebar.download_button("⬇️ Income Statement CSV", csv_income, "income_statement.csv", "text/csv")
st.sidebar.download_button("⬇️ Balance Sheet CSV", csv_balance, "balance_sheet.csv", "text/csv")

st.sidebar.info("Data sources:audited annual reports 2021–2025.")
