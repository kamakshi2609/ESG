import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="AI ESG Market Analytics", layout="wide")

st.title("🌍 AI-Driven Real-Time ESG Market Analytics Dashboard")

company = st.text_input("Enter Company Ticker (e.g., RELIANCE.NS, TCS.NS, AAPL)")

if st.button("Analyze ESG Performance"):

    if company == "":
        st.warning("Please enter a valid ticker.")
    else:
        with st.spinner("Fetching real-time market data..."):

            try:
                stock = yf.Ticker(company)
                hist = stock.history(period="1y")

                if hist.empty:
                    st.error("Invalid ticker or no data available.")
                else:

                    # -------------------------
                    # Feature Engineering
                    # -------------------------
                    hist["returns"] = hist["Close"].pct_change()

                    volatility = hist["returns"].std() * np.sqrt(252)
                    mean_return = hist["returns"].mean() * 252
                    sharpe_ratio = mean_return / (volatility + 1e-6)

                    # Normalize Scores
                    vol_score = 1 / (1 + volatility * 8)
                    return_score = np.clip((mean_return + 0.2) / 0.4, 0, 1)
                    sharpe_score = np.clip((sharpe_ratio + 2) / 4, 0, 1)

                    esg_score = (
                        vol_score * 35 +
                        return_score * 30 +
                        sharpe_score * 35
                    )

                    esg_score = float(np.clip(esg_score, 0, 100))

                    # -------------------------
                    # ESG Gauge
                    # -------------------------
                    st.markdown("## 🌍 ESG Proxy Score")

                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=esg_score,
                        title={'text': "ESG Proxy Score"},
                        gauge={
                            'axis': {'range': [0, 100]},
                            'steps': [
                                {'range': [0, 50], 'color': "red"},
                                {'range': [50, 75], 'color': "yellow"},
                                {'range': [75, 100], 'color': "green"}
                            ],
                        }
                    ))

                    st.plotly_chart(fig, use_container_width=True)

                    # -------------------------
                    # Impact Analysis
                    # -------------------------
                    st.markdown("## 📉 Impact Analysis")

                    if esg_score >= 75:
                        risk = "Low"
                        investor_confidence = "High"
                        regulatory_pressure = "Low"
                    elif esg_score >= 50:
                        risk = "Moderate"
                        investor_confidence = "Stable"
                        regulatory_pressure = "Medium"
                    else:
                        risk = "High"
                        investor_confidence = "Low"
                        regulatory_pressure = "High"

                    col1, col2, col3 = st.columns(3)
                    col1.metric("Financial Risk", risk)
                    col2.metric("Investor Confidence", investor_confidence)
                    col3.metric("Regulatory Exposure", regulatory_pressure)

                    # -------------------------
                    # Charts Section
                    # -------------------------

                    st.markdown("## 📊 Market Behaviour Analysis")

                    # Moving Average
                    hist["MA50"] = hist["Close"].rolling(50).mean()

                    st.subheader("📈 Price Trend with 50-Day Moving Average")
                    st.line_chart(hist[["Close", "MA50"]])

                    # Rolling Volatility
                    hist["rolling_vol"] = hist["returns"].rolling(30).std() * np.sqrt(252)
                    st.subheader("⚠ Rolling Volatility (Risk Trend)")
                    st.line_chart(hist["rolling_vol"])

                    # Cumulative Returns
                    hist["cumulative_return"] = (1 + hist["returns"]).cumprod()
                    st.subheader("💰 Cumulative Return (₹1 Investment Growth)")
                    st.line_chart(hist["cumulative_return"])

                    # -------------------------
                    # AI Insight
                    # -------------------------
                    st.markdown("## 🤖 AI Sustainability Insight")

                    insight = f"""
                    Based on 1-year market performance, {company} demonstrates:

                    • Annual Volatility: {round(volatility,3)}  
                    • Annual Return: {round(mean_return*100,2)}%  
                    • Sharpe Ratio: {round(sharpe_ratio,2)}  

                    The ESG proxy score of {round(esg_score,2)} reflects
                    risk-adjusted stability and market-based sustainability signals.

                    Companies with lower volatility and higher Sharpe ratios
                    indicate stronger governance discipline and long-term resilience.
                    """

                    st.write(insight)

            except Exception:
                st.error("Data fetch failed. Try another ticker or try again later.")
