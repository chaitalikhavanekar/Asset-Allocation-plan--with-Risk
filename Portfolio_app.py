# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
from textwrap import wrap

# -------------------------
# Page config
# -------------------------
st.set_page_config(page_title="Asset Allocation Dashboard", layout="wide", initial_sidebar_state="auto")

# -------------------------
# Styling (TaxBase-inspired)
# -------------------------
st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
    :root{
      --bg-top:#0f3a34;        /* deep forest tone */
      --bg-bottom:#173f3a;     /* softer graphite */
      --accent-gold:#E9C46A;   /* gold accent */
      --ivory:#F4F4F2;         /* main text */
      --soft-silver:#D8D8D8;   /* secondary text */
      --glass: rgba(255,255,255,0.04);
    }
    /* app background */
    [data-testid="stAppViewContainer"]{
      background: linear-gradient(180deg, var(--bg-top) 0%, var(--bg-bottom) 100%);
      color: var(--ivory);
      font-family: 'Poppins', sans-serif;
    }
    /* header */
    .big-title {
      font-size: 34px;
      font-weight: 700;
      color: var(--ivory);
      margin-bottom: 6px;
    }
    .subtitle {
      color: var(--soft-silver);
      margin-top: 0px;
      margin-bottom: 18px;
    }
    /* sidebar */
    [data-testid="stSidebar"]{
      background: linear-gradient(180deg, rgba(10,20,20,0.95), rgba(14,28,28,0.92));
      border-right: 1px solid rgba(255,255,255,0.04);
    }
    /* dataframe glass */
    [data-testid="stDataFrame"] table {
      border-radius: 10px;
      background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
      border: 1px solid rgba(233,196,106,0.06);
      overflow: hidden;
    }
    [data-testid="stDataFrame"] th {
      background: rgba(233,196,106,0.12) !important;
      color: #071b19 !important;
      font-weight: 600;
      text-align:center;
    }
    [data-testid="stDataFrame"] td {
      color: var(--ivory) !important;
      text-align:center;
      padding: 6px 8px;
      font-size: 14px;
    }
    /* metrics */
    .metric-span {
      color: var(--accent-gold);
      font-weight: 700;
      font-size: 18px;
    }
    /* AI summary box */
    .ai-box {
      background: rgba(10,12,12,0.55);
      border-radius: 10px;
      border: 1px solid rgba(233,196,106,0.12);
      padding: 16px;
      color: var(--ivory);
      box-shadow: 0 6px 18px rgba(0,0,0,0.45);
      font-size: 15px;
      line-height: 1.5;
    }
    .ai-title {
      color: var(--accent-gold);
      font-weight: 700;
      margin-bottom: 6px;
      font-size: 16px;
    }
    .muted {
      color: var(--soft-silver);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# Title and subtitle
# -------------------------
st.markdown('<div class="big-title">Asset Allocation Portfolio Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Visualize low / moderate / high risk portfolios with clear tables, pro charts, and an AI-style summary panel.</div>', unsafe_allow_html=True)

# -------------------------
# Data (keeps your original logic & summary text)
# -------------------------
data = {
    "Low Risk (45–65)": pd.DataFrame({
        "Asset Class": ["Equity (Stocks / MFs)", "Debt / Fixed Income", "Gold / Commodities", "Real Estate", "Cash / Liquid Funds"],
        "Allocation (%)": [15, 50, 20, 10, 5],
        "Risk": ["Moderate", "Low", "Moderate", "Low moderate", "Very low"],
        "Reward (Expected)": ["9%–11%", "6%–7%", "8%–9%", "6%–8%", "3%–4%"],
        "Time Period": ["5–7 YRS", "3–5 YRS", "7–10 YRS", "3–5 YRS", "0–1 YRS"],
        "Portfolio Weight Impact (%)": [15, 50, 20, 10, 5],
        "LOGIC": [
            "Stock market fluctuates; you can lose 20–30% value in short term. But since only 15% is invested, overall portfolio impact is ~10%.",
            "Safer because returns are fixed. Risk comes only if interest rates change or company defaults (rare if chosen wisely).",
            "Prices move up/down with global economy, but gold always regains in long term; protects during crises.",
            "Property isn't easy to sell quickly; market cycles can take years. Physical asset = safe long-term.",
            "Almost risk-free, but inflation slowly reduces its real value."
        ],
        "SUMMARY": [
            "Keeps inflation protection and long-term growth, but limits volatility.",
            "Main stability pillar; ensures predictable cash flow and acts as shock absorber.",
            "Protects capital during downturns; hedge against equity risk.",
            "Illiquid but steady; useful as diversification for long-term wealth.",
            "For liquidity in emergencies or reinvestment when markets dip."
        ]
    }),

    "Moderate Risk (30–45)": pd.DataFrame({
        "Asset Class": ["Equity (Stocks / MFs)", "Debt / Fixed Income", "Real Estate", "Gold / Commodities", "Cash / Liquid Funds"],
        "Allocation (%)": [40, 35, 15, 7, 3],
        "Risk": ["High", "Low", "Moderate", "Moderate", "Very low"],
        "Reward (Expected)": ["11%–13%", "6%–7%", "8%–9%", "8%", "3%–4%"],
        "Time Period": ["7–10 YRS", "3–5 YRS", "7–10 YRS", "3–5 YRS", "0–1 YRS"],
        "Portfolio Weight Impact (%)": [40, 35, 15, 7, 3],
        "LOGIC": [
            "People in their 30s–40s can handle volatility since they have longer time horizons. Equity gives growth and beats inflation.",
            "Ensures portfolio stability and consistent returns. Balances market swings from equity.",
            "Diversifies portfolio; suitable for long-term wealth building and rental potential.",
            "Gold acts as a hedge against market downturns and inflation.",
            "Maintains liquidity for opportunities or emergencies."
        ],
        "SUMMARY": [
            "Main wealth generator; short-term volatility balanced by long-term compounding.",
            "Provides steady income, reduces portfolio shocks, keeps capital partly protected.",
            "Tangible asset that provides inflation-adjusted growth though less liquid.",
            "Keeps portfolio stable during uncertainty; small allocation is enough.",
            "Helps during emergencies or reinvestment opportunities; avoids cash drag."
        ]
    }),

    "High Risk (25–30)": pd.DataFrame({
        "Asset Class": ["Equity (Stocks / MFs)", "Debt / Fixed Income", "Gold / Commodities", "Real Estate", "Cash / Liquid Funds"],
        "Allocation (%)": [60, 15, 10, 10, 5],
        "Risk": ["High", "Low", "Moderate", "Moderate", "Very low"],
        "Reward (Expected)": ["12%–14%", "6%–7%", "8%–9%", "9%–10%", "3%–4%"],
        "Time Period": ["7–10 YRS", "1–3 YRS", "5–7 YRS", "7–10 YRS", "0–1 YRS"],
        "Portfolio Weight Impact (%)": [60, 15, 10, 10, 5],
        "LOGIC": [
            "Long-term horizon allows high stock exposure. Short-term volatility (−20% to +30%) is tolerable because recovery over years gives compounding power.",
            "Offers stability to offset market dips and provides liquidity for short-term needs.",
            "Hedge against inflation, currency weakening, and equity crashes.",
            "Provides tangible asset diversification and potential rental income.",
            "Used for emergency fund and quick opportunities during market dips."
        ],
        "SUMMARY": [
            "Core growth engine — maximizes wealth creation through market cycles.",
            "Acts as portfolio stabilizer to reduce panic during volatility.",
            "Adds diversification and protection in global uncertainty.",
            "Long-term capital appreciation; less liquid but inflation-beating.",
            "Ensures liquidity without disturbing long-term holdings."
        ]
    })
}

# -------------------------
# Risk metrics (kept from your sheet)
# -------------------------
metrics = {
    "Low Risk (45–65)": {"Expected Return": "7.95%", "Risk (Std. Dev.)": "9.90%", "Worst (95%)": "-11%", "Best (95%)": "27%", "Sharpe-like": "0.80"},
    "Moderate Risk (30–45)": {"Expected Return": "9.00%", "Risk (Std. Dev.)": "11.30%", "Worst (95%)": "-13%", "Best (95%)": "31%", "Sharpe-like": "0.80"},
    "High Risk (25–30)": {"Expected Return": "10.75%", "Risk (Std. Dev.)": "19.60%", "Worst (95%)": "-28%", "Best (95%)": "50%", "Sharpe-like": "0.55"}
}

# -------------------------
# Sources table
# -------------------------
sources = pd.DataFrame({
    "Asset": ["Equity (Nifty/Sensex)", "Debt (Govt + Corporate)", "Gold", "Real Estate", "Cash/FD"],
    "Historical Return": ["11–13%", "6–8%", "7–9%", "8–10%", "4–5%"],
    "Volatility": ["12–18%", "3–5%", "10–12%", "8–10%", "<1%"],
    "Source": ["15-year CAGR of Indian Equity Market", "Average yield-to-maturity of debt (2010–2024)", "RBI & World Gold Council long-term data", "Knight Frank + RBI housing index", "Bank FD rates (SBI, HDFC, ICICI)"]
})

# -------------------------
# Sidebar controls
# -------------------------
st.sidebar.header("Portfolio Controls")
profile = st.sidebar.selectbox("Select Risk Profile", list(data.keys()))
chart_type = st.sidebar.selectbox("Chart type", ["Bar", "Pie", "3D Scatter"])
animate = st.sidebar.checkbox("Enable animation (pie/bar live redraw)", value=True)
show_typing = st.sidebar.checkbox("Show AI summary typing", value=True)
years = st.sidebar.slider("Projection horizon (years) for simple growth simulation", 1, 20, 10)

# -------------------------
# Current DataFrame
# -------------------------
df = data[profile].copy()

# center area layout
left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader(f"Portfolio Overview — {profile}")
    st.markdown("<div style='color: #D8D8D8; margin-bottom:6px;'>Full table with logic and summary retained (readable)</div>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)

    # small simulation: projected growth using expected return (convert simple)
    base_return_map = {"Low Risk (45–65)": 0.0795, "Moderate Risk (30–45)": 0.09, "High Risk (25–30)": 0.1075}
    base_return = base_return_map[profile]
    years_range = list(range(0, years + 1))
    growth = [(1 + base_return) ** y for y in years_range]
    sim_df = pd.DataFrame({"Year": years_range, "Index (Base=100)": np.round(100 * np.array(growth), 2)})

    st.markdown("### Projection (simple compound growth)")
    fig_proj = px.line(sim_df, x="Year", y="Index (Base=100)", markers=True, title=f"Projection ({int(base_return*100)}% base return) over {years} yrs",
                       template="plotly_dark")
    fig_proj.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                           font=dict(color="#F4F4F2"))
    st.plotly_chart(fig_proj, use_container_width=True)

with right_col:
    st.subheader("Performance Metrics")
    m = metrics[profile]
    cols = st.columns(len(m))
    for i, (k, v) in enumerate(m.items()):
        cols[i].metric(k, v)

# -------------------------
# Charts (main)
# -------------------------
st.markdown("### Allocation Visuals")
chart_col1, chart_col2 = st.columns([1, 1])

palette = {
    "Equity (Stocks / MFs)": "#D4A373",  # muted gold
    "Equity": "#D4A373",
    "Debt / Fixed Income": "#4CB5AE",    # teal
    "Debt": "#4CB5AE",
    "Gold / Commodities": "#C08B4E",     # coppery
    "Gold": "#C08B4E",
    "Real Estate": "#9DA3B4",            # steel
    "Cash / Liquid Funds": "#CED4DA",    # light grey
    "Cash": "#CED4DA"
}

# Prepare values & labels (handle multiple naming)
labels = df["Asset Class"].tolist()
values = df["Allocation (%)"].tolist()

if chart_type == "Pie":
    # animate by re-drawing small steps (if enabled)
    if animate:
        placeholder = st.empty()
        for step in range(3):
            # small random jitter to create subtle movement
            jitter = np.random.randint(-2, 3, len(values))
            cur_vals = np.clip(np.array(values) + jitter, 1, 100)
            fig = px.pie(names=labels, values=cur_vals, hole=0.35)
            fig.update_traces(textinfo='percent+label', marker=dict(colors=[palette.get(l.split(' ')[0], "#8AA4A8") for l in labels]))
            fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                              title=f"Allocation — {profile}")
            placeholder.plotly_chart(fig, use_container_width=True)
            time.sleep(0.25)
    else:
        fig = px.pie(names=labels, values=values, hole=0.35)
        fig.update_traces(textinfo='percent+label', marker=dict(colors=[palette.get(l.split(' ')[0], "#8AA4A8") for l in labels]))
        fig.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                          title=f"Allocation — {profile}")
        chart_col1.plotly_chart(fig, use_container_width=True)

elif chart_type == "Bar":
    fig = px.bar(df, x="Asset Class", y="Allocation (%)", text="Allocation (%)",
                 color="Asset Class", category_orders={"Asset Class": labels})
    fig.update_traces(marker_color=[palette.get(l.split(' ')[0], "#8AA4A8") for l in labels], showlegend=False)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title=f"Allocation — {profile}",
                      xaxis_title="", yaxis_title="Allocation (%)")
    chart_col1.plotly_chart(fig, use_container_width=True)
else:
    # 3D scatter: Allocation vs Risk Score vs Reward %
    # map textual Risk -> score
    risk_map = {"Very low": 1, "Very Low":1, "Low": 2, "Low moderate":3, "Low-Moderate":3, "Moderate":4, "High":5}
    df_plot = df.copy()
    df_plot["Risk Score"] = df_plot["Risk"].map(risk_map).fillna(3)
    # extract reward numeric
    def extract_reward(x):
        s = str(x)
        digits = ''.join(ch for ch in s if ch.isdigit())
        return float(digits) if digits else 0.0
    df_plot["Reward %"] = df_plot["Reward (Expected)"].apply(extract_reward)
    fig3d = go.Figure(data=[go.Scatter3d(
        x=df_plot["Allocation (%)"],
        y=df_plot["Risk Score"],
        z=df_plot["Reward %"],
        text=df_plot["Asset Class"],
        mode='markers+text',
        marker=dict(size=9, color=df_plot["Allocation (%)"], colorscale='Viridis', opacity=0.9)
    )])
    fig3d.update_layout(scene=dict(xaxis_title='Allocation (%)', yaxis_title='Risk Score', zaxis_title='Reward (%)'),
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', title=f"3D Risk-Reward — {profile}")
    chart_col1.plotly_chart(fig3d, use_container_width=True)

# right-side smaller chart
chart_col2.markdown("#### Allocation Breakdown (table)")
# small spark table
chart_col2.table(df[["Asset Class", "Allocation (%)"]].set_index("Asset Class"))

# -------------------------
# AI summary typing box
# -------------------------
st.markdown("### AI Analysis")
ai_col1, ai_col2 = st.columns([2, 1])

with ai_col1:
    if show_typing:
        # Build a combined human-readable summary from the SUMMARY column (preserve original text)
        # We'll craft a coherent paragraph: start with portfolio name, then join each summary sentence.
        summary_lines = df["SUMMARY"].tolist()
        # combine but keep short sentences
        combined = f"{profile} — " + " ".join([s.strip() for s in summary_lines if isinstance(s, str)])
        # typing animation into a placeholder
        placeholder_text = st.empty()
        typed = ""
        delay = 0.01  # speed of typing (seconds per char)
        for ch in combined:
            typed += ch
            placeholder_text.markdown(f"<div class='ai-box'><div class='ai-title'>System Analysis</div><div class='muted'>Generated insight (automated)</div><br><div>{typed}</div></div>", unsafe_allow_html=True)
            time.sleep(delay)
        # final write to ensure stable
        placeholder_text.markdown(f"<div class='ai-box'><div class='ai-title'>System Analysis</div><div class='muted'>Generated insight (automated)</div><br><div>{combined}</div></div>", unsafe_allow_html=True)
    else:
        combined = f"{profile} — " + " ".join([s.strip() for s in df["SUMMARY"].tolist() if isinstance(s, str)])
        st.markdown(f"<div class='ai-box'><div class='ai-title'>System Analysis</div><div class='muted'>Generated insight (automated)</div><br><div>{combined}</div></div>", unsafe_allow_html=True)

with ai_col2:
    st.markdown("#### Quick Actions")
    st.markdown("- Download table (CSV)")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, file_name=f"{profile.replace(' ','_')}.csv", mime="text/csv")
    st.markdown("")
    st.markdown("#### Sources")
    st.markdown("<div class='muted'>Data references used to form reward/risk bands</div>", unsafe_allow_html=True)
    st.dataframe(sources, use_container_width=True)

# -------------------------
# Footer
# -------------------------
st.markdown("<br><hr style='border:1px solid rgba(255,255,255,0.04)'>", unsafe_allow_html=True)
st.markdown("<div style='color: #D8D8D8; font-size:13px;'>Made with care by <b>Chaitali Khavanekar</b> — Portfolio models are illustrative. Consult a financial advisor before investing.</div>", unsafe_allow_html=True)
