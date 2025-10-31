import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Asset Allocation Dashboard", layout="wide")

# ---------- CUSTOM DESIGN ----------
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
<style>
body {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(135deg, #121212, #1a1a2e, #16213e);
    color: #f1f1f1;
}

/* Header */
h1 {
    color: #00d4ff;
    font-weight: 700;
    font-size: 38px;
    text-align: center;
    padding-bottom: 0.3em;
    border-bottom: 2px solid #00d4ff;
    margin-bottom: 0.8em;
    letter-spacing: 1px;
}

/* Subheaders */
h2, h3 {
    color: #00e6ac;
    font-weight: 600;
    margin-top: 25px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: rgba(20, 20, 40, 0.95);
    border-right: 2px solid #00bcd4;
    box-shadow: 4px 0 15px rgba(0, 188, 212, 0.2);
}

/* DataFrame table style */
[data-testid="stDataFrame"] table {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    border-collapse: collapse;
    overflow: hidden;
}

[data-testid="stDataFrame"] th {
    background: #00d4ff;
    color: black;
    font-weight: bold;
    text-align: center;
}

[data-testid="stDataFrame"] td {
    text-align: center;
    color: #e8e8e8;
    padding: 6px;
}

/* Metric cards */
[data-testid="stMetricValue"] {
    color: #00ffd0 !important;
    font-weight: 700;
    font-size: 20px;
}

/* Expander */
[data-testid="stExpander"] {
    background-color: rgba(20, 20, 40, 0.8);
    border: 1px solid #00bcd4;
    border-radius: 10px;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown("<h1>💼 Asset Allocation Portfolio Dashboard</h1>", unsafe_allow_html=True)
st.markdown("#### 📊 Visualize risk, reward & diversification with elegant charts and analytics.")

# ---------- DATA ----------
data = {
    "Low Risk (45–65)": pd.DataFrame({
        "Asset Class": ["Equity", "Debt", "Gold", "Real Estate", "Cash"],
        "Allocation": [15, 50, 20, 10, 5],
        "Risk": ["Moderate", "Low", "Moderate", "Low-Moderate", "Very Low"],
        "Reward": ["9–11%", "6–7%", "8–9%", "6–8%", "3–4%"],
        "Time Period": ["5–7 yrs", "3–5 yrs", "7–10 yrs", "3–5 yrs", "0–1 yrs"],
        "Logic": [
            "Equities provide moderate exposure to growth.",
            "Debt ensures capital safety and steady returns.",
            "Gold protects against inflation shocks.",
            "Real estate adds tangible diversification.",
            "Cash ensures liquidity."
        ],
        "Summary": [
            "Stable and defensive portfolio for capital preservation.",
            "Ideal for conservative investors seeking low volatility.",
            "Provides safety with some inflation-adjusted growth.",
            "Limited growth, high stability and liquidity."
        ]
    }),

    "Moderate Risk (30–45)": pd.DataFrame({
        "Asset Class": ["Equity", "Debt", "Real Estate", "Gold", "Cash"],
        "Allocation": [40, 35, 15, 7, 3],
        "Risk": ["High", "Low", "Moderate", "Moderate", "Very Low"],
        "Reward": ["11–13%", "6–7%", "8–9%", "8%", "3–4%"],
        "Time Period": ["7–10 yrs", "3–5 yrs", "7–10 yrs", "3–5 yrs", "0–1 yrs"],
        "Logic": [
            "Equities drive long-term wealth creation.",
            "Debt balances volatility.",
            "Real estate adds tangible asset growth.",
            "Gold acts as inflation hedge.",
            "Cash keeps flexibility."
        ],
        "Summary": [
            "Balanced and growth-oriented portfolio for mid-term goals."
        ]
    }),

    "High Risk (25–30)": pd.DataFrame({
        "Asset Class": ["Equity", "Debt", "Gold", "Real Estate", "Cash"],
        "Allocation": [60, 15, 10, 10, 5],
        "Risk": ["High", "Low", "Moderate", "Moderate", "Very Low"],
        "Reward": ["12–14%", "6–7%", "8–9%", "9–10%", "3–4%"],
        "Time Period": ["7–10 yrs", "1–3 yrs", "5–7 yrs", "7–10 yrs", "0–1 yrs"],
        "Logic": [
            "Equity is the major growth engine.",
            "Debt adds safety layer.",
            "Gold diversifies risk.",
            "Real estate offers long-term appreciation.",
            "Cash for liquidity buffer."
        ],
        "Summary": [
            "Aggressive growth portfolio for long-term compounding."
        ]
    })
}

# ---------- RISK METRICS ----------
metrics = {
    "Low Risk (45–65)": {"Expected Return": "7.95%", "Risk": "9.9%", "Worst": "-11%", "Best": "27%"},
    "Moderate Risk (30–45)": {"Expected Return": "9.0%", "Risk": "11.3%", "Worst": "-13%", "Best": "31%"},
    "High Risk (25–30)": {"Expected Return": "10.75%", "Risk": "19.6%", "Worst": "-28%", "Best": "50%"}
}

# ---------- APP UI ----------
profile = st.sidebar.selectbox("🎯 Choose Risk Profile", list(data.keys()))
chart_type = st.sidebar.selectbox("📊 Choose Chart Type", ["Bar Chart", "Pie Chart", "3D Chart"])
df = data[profile]

# ---------- DISPLAY DATA ----------
st.markdown(f"### 🧾 Portfolio Overview: {profile}")
st.dataframe(df, use_container_width=True)

# ---------- CHARTS ----------
if chart_type == "Bar Chart":
    fig = px.bar(df, x="Asset Class", y="Allocation", color="Risk", text="Allocation", color_discrete_sequence=px.colors.sequential.Tealgrn)
elif chart_type == "Pie Chart":
    fig = px.pie(df, names="Asset Class", values="Allocation", hole=0.35, color_discrete_sequence=px.colors.sequential.Teal)
else:
    # 3D Chart – Allocation vs Reward vs Risk
    risk_map = {"Very Low": 1, "Low": 2, "Low-Moderate": 3, "Moderate": 4, "High": 5}
    df["Risk Score"] = df["Risk"].map(risk_map)
    df["Reward %"] = df["Reward"].str.replace("%", "").str.extract("(\d+)").astype(float)
    fig = go.Figure(data=[go.Scatter3d(
        x=df["Allocation"],
        y=df["Risk Score"],
        z=df["Reward %"],
        mode='markers+text',
        text=df["Asset Class"],
        marker=dict(size=10, color=df["Risk Score"], colorscale='Viridis', opacity=0.9)
    )])
    fig.update_layout(scene=dict(
        xaxis_title='Allocation (%)',
        yaxis_title='Risk Level',
        zaxis_title='Reward (%)',
        bgcolor="rgba(10,10,20,0.8)"
    ))

fig.update_layout(title=f"{chart_type} — {profile}", title_x=0.4, plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig, use_container_width=True)

# ---------- METRICS ----------
st.markdown("### 📈 Performance Summary")
cols = st.columns(len(metrics[profile]))
for i, (k, v) in enumerate(metrics[profile].items()):
    cols[i].metric(k, v)

# ---------- SOURCES ----------
with st.expander("📚 Data Sources & References"):
    st.write("""
    - Equity data: Nifty/Sensex CAGR (15 years)
    - Debt: RBI & SEBI bond returns
    - Gold: World Gold Council, RBI Data
    - Real Estate: Knight Frank Housing Index
    - Cash: Major bank FD rates (SBI, HDFC, ICICI)
    """)

st.markdown("<br><center>✨ Made with precision by <b>Chaitali Khavanekar</b></center>", unsafe_allow_html=True)
