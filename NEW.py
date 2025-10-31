import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Asset Allocation Dashboard", layout="wide")

st.title("💼 Asset Allocation Portfolio Dashboard")
st.markdown("Compare risk profiles, asset weights, and returns with interactive visuals and logic insights.")

# ----- DATA -----
data = {
    "Low Risk (45–65)": pd.DataFrame({
        "Asset Class": ["Equity (Stocks / MFs)", "Debt / Fixed Income", "Gold / Commodities", "Real Estate", "Cash / Liquid Funds"],
        "Allocation": [15, 50, 20, 10, 5],
        "Risk": ["Moderate", "Low", "Moderate", "Low-Moderate", "Very Low"],
        "Reward": ["9–11%", "6–7%", "8–9%", "6–8%", "3–4%"],
        "Time Period": ["5–7 yrs", "3–5 yrs", "7–10 yrs", "3–5 yrs", "0–1 yrs"],
        "Portfolio Impact": [15, 50, 20, 10, 5],
        "Logic": [
            "Stock market fluctuates; limited impact at 15%.",
            "Safer base; returns stable; main stability pillar.",
            "Hedge during inflation; long-term safe asset.",
            "Illiquid but steady long-term value.",
            "Used for liquidity or reinvestment."
        ],
        "Summary": [
            "Inflation protection but limited growth.",
            "Predictable cash flow, low volatility.",
            "Moves opposite to equity; protects during crises.",
            "Common Indian asset; low liquidity.",
            "Useful for emergencies."
        ]
    }),

    "Moderate Risk (30–45)": pd.DataFrame({
        "Asset Class": ["Equity (Stocks / MFs)", "Debt / Fixed Income", "Real Estate", "Gold / Commodities", "Cash / Liquid Funds"],
        "Allocation": [40, 35, 15, 7, 3],
        "Risk": ["High", "Low", "Moderate", "Moderate", "Very Low"],
        "Reward": ["11–13%", "6–7%", "8–9%", "8%", "3–4%"],
        "Time Period": ["7–10 yrs", "3–5 yrs", "7–10 yrs", "3–5 yrs", "0–1 yrs"],
        "Portfolio Impact": [40, 35, 15, 7, 3],
        "Logic": [
            "Younger investors can handle volatility; long horizon helps compounding.",
            "Ensures portfolio stability; reduces swings.",
            "Diversifies and adds inflation-adjusted growth.",
            "Acts as hedge during uncertainty.",
            "Maintains liquidity for emergencies."
        ],
        "Summary": [
            "Wealth generator; balanced by long-term compounding.",
            "Provides steady income and stability.",
            "Inflation-adjusted tangible asset.",
            "Adds safety; protects against downturns.",
            "Avoids cash drag; useful for opportunities."
        ]
    }),

    "High Risk (25–30)": pd.DataFrame({
        "Asset Class": ["Equity (Stocks / MFs)", "Debt / Fixed Income", "Gold / Commodities", "Real Estate", "Cash / Liquid Funds"],
        "Allocation": [60, 15, 10, 10, 5],
        "Risk": ["High", "Low", "Moderate", "Moderate", "Very Low"],
        "Reward": ["12–14%", "6–7%", "8–9%", "9–10%", "3–4%"],
        "Time Period": ["7–10 yrs", "1–3 yrs", "5–7 yrs", "7–10 yrs", "0–1 yrs"],
        "Portfolio Impact": [60, 15, 10, 10, 5],
        "Logic": [
            "Long-term exposure; short-term volatility tolerable.",
            "Stabilizer to offset equity dips.",
            "Diversifies global uncertainty impact.",
            "Adds tangible diversification and rental income.",
            "Emergency liquidity buffer."
        ],
        "Summary": [
            "Maximizes compounding; suited for long-term growth.",
            "Reduces panic in volatile years.",
            "Protection from global inflation shocks.",
            "Inflation-beating, less liquid asset.",
            "Quick fund for emergencies."
        ]
    })
}

# ----- RISK–RETURN METRICS -----
metrics = {
    "Low Risk (45–65)": {
        "Expected Return": "7.95%", "Risk": "9.9%", "Worst": "-11%", "Best": "27%", "Sharpe-like": "0.80"
    },
    "Moderate Risk (30–45)": {
        "Expected Return": "9.0%", "Risk": "11.3%", "Worst": "-13%", "Best": "31%", "Sharpe-like": "0.80"
    },
    "High Risk (25–30)": {
        "Expected Return": "10.75%", "Risk": "19.6%", "Worst": "-28%", "Best": "50%", "Sharpe-like": "0.55"
    }
}

# ----- SOURCES -----
sources = pd.DataFrame({
    "Asset": ["Equity (Nifty/Sensex)", "Debt (Govt + Corporate)", "Gold", "Real Estate", "Cash/FD"],
    "Historical Return": ["11–13%", "6–8%", "7–9%", "8–10%", "4–5%"],
    "Volatility": ["12–18%", "3–5%", "10–12%", "8–10%", "<1%"],
    "Source": [
        "15-year CAGR of Indian Equity Market",
        "Average YTM (2010–2024)",
        "RBI & World Gold Council Data",
        "Knight Frank + RBI Housing Index",
        "Bank FD Rates (SBI, HDFC, ICICI)"
    ]
})

# ----- APP UI -----
profile = st.sidebar.selectbox("Select Risk Profile", list(data.keys()))
chart_type = st.sidebar.selectbox("Select Chart Type", ["Bar Chart", "Pie Chart", "Line Chart"])
animate = st.sidebar.checkbox("Enable Chart Animation", value=True)

df = data[profile]
st.subheader(f"📊 {profile} Portfolio Overview")

# ----- MAIN TABLE -----
st.dataframe(df, use_container_width=True)

# ----- CHART -----
if chart_type == "Bar Chart":
    fig = px.bar(df, x="Asset Class", y="Allocation", color="Risk",
                 text="Allocation", animation_frame="Time Period" if animate else None)
elif chart_type == "Pie Chart":
    fig = px.pie(df, names="Asset Class", values="Allocation", color="Risk",
                 hole=0.3)
else:
    fig = px.line(df, x="Asset Class", y="Allocation", markers=True, color="Risk")

fig.update_layout(title=f"{chart_type} — {profile}", title_x=0.3)
st.plotly_chart(fig, use_container_width=True)

# ----- RISK–RETURN METRICS -----
st.markdown("### 📈 Portfolio Performance Summary")
metric = metrics[profile]
cols = st.columns(len(metric))
for i, (key, val) in enumerate(metric.items()):
    cols[i].metric(key, val)

# ----- SOURCES -----
with st.expander("📚 Data Sources & References"):
    st.dataframe(sources, use_container_width=True)

st.markdown("Made with ❤️ by Chaitali Khavanekar")
