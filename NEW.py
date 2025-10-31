import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import time

st.set_page_config(page_title="Asset Allocation Dashboard", layout="wide")

# ----------------------------
# Title
# ----------------------------
st.title("💹 Asset Allocation Dashboard")
st.write("An interactive tool to explore portfolio allocations across different **risk profiles** and visualize expected performance over time.")

# ----------------------------
# Sidebar Controls
# ----------------------------
st.sidebar.header("⚙️ Portfolio Filter")
risk_profile = st.sidebar.selectbox("Select Risk Profile", ["Low", "Moderate", "High"])
animate = st.sidebar.checkbox("Show live animation", value=False)

# ----------------------------
# Data (from your sheets)
# ----------------------------
data = {
    "Low": pd.DataFrame({
        "Asset Class": ["Equity (Stocks / MFs)", "Debt / Fixed Income", "Gold / Commodities", "Real Estate", "Cash / Liquid Funds"],
        "Allocation (%)": [15, 50, 20, 10, 5],
        "Risk": ["Moderate", "Low", "Moderate", "Low-Moderate", "Very Low"],
        "Reward": ["9–11%", "6–7%", "8–9%", "6–8%", "3–4%"]
    }),
    "Moderate": pd.DataFrame({
        "Asset Class": ["Equity (Stocks / MFs)", "Debt / Fixed Income", "Real Estate", "Gold / Commodities", "Cash / Liquid Funds"],
        "Allocation (%)": [40, 35, 15, 7, 3],
        "Risk": ["High", "Low", "Moderate", "Moderate", "Very Low"],
        "Reward": ["11–13%", "6–7%", "8–9%", "8%", "3–4%"]
    }),
    "High": pd.DataFrame({
        "Asset Class": ["Equity (Stocks / MFs)", "Debt / Fixed Income", "Gold / Commodities", "Real Estate", "Cash / Liquid Funds"],
        "Allocation (%)": [60, 15, 10, 10, 5],
        "Risk": ["High", "Low", "Moderate", "Moderate", "Very Low"],
        "Reward": ["12–14%", "6–7%", "8–9%", "9–10%", "3–4%"]
    })
}

# ----------------------------
# Display Table
# ----------------------------
df = data[risk_profile]
st.subheader(f"📊 {risk_profile} Risk Portfolio Allocation")
st.dataframe(df, use_container_width=True)

# ----------------------------
# Chart Section
# ----------------------------
st.markdown("### 📈 Allocation Breakdown")

# Animated or static chart
if animate:
    placeholder = st.empty()
    values = df["Allocation (%)"].values
    labels = df["Asset Class"].values

    # Animate change in allocation (simulated)
    for step in range(1, 11):
        new_values = values + np.random.randint(-2, 3, len(values))
        new_values = np.clip(new_values, 0, 100)
        fig = px.pie(values=new_values, names=labels, title=f"Animated Allocation — Step {step}")
        fig.update_traces(textinfo="percent+label", pull=[0.05]*len(labels))
        placeholder.plotly_chart(fig, use_container_width=True)
        time.sleep(0.7)
else:
    fig = px.pie(df, values="Allocation (%)", names="Asset Class", title=f"{risk_profile} Risk Portfolio Allocation")
    fig.update_traces(textinfo="percent+label", pull=[0.05]*len(df))
    st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# Performance Simulation
# ----------------------------
st.markdown("### 📊 Simulated Growth Over Time")

years = st.slider("Select Time Horizon (Years)", 1, 20, 10)
base_return = {"Low": 0.0795, "Moderate": 0.09, "High": 0.1075}[risk_profile]
growth = [(1 + base_return) ** i for i in range(years + 1)]
df_growth = pd.DataFrame({"Year": list(range(years + 1)), "Portfolio Value (₹)": np.array(growth) * 100})

fig2 = px.line(df_growth, x="Year", y="Portfolio Value (₹)", markers=True,
               title=f"Projected Portfolio Growth ({risk_profile} Risk)")
st.plotly_chart(fig2, use_container_width=True)

st.success("💰 Tip: Diversify across asset classes to balance return and risk.")
