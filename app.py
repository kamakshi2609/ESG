import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd

st.set_page_config(page_title="Real-Time ESG Proxy Analyzer", layout="centered")

st.title("🌍 AI-Based Real-Time ESG Proxy Analyzer")

company = st.text_input("Enter Company Ticker (e.g., RELIANCE.NS, TCS.NS, AAPL)")

if st.button("Analyze ESG Performance"):

    if company == "":
        st.warning("Please enter a company ticker.")
    else:
        with st.spinner("Fetching real-time market data..."):

            try:
                stock = yf.Ticker(company)
                hist = stock.history(period="1y")

                if hist.empty:
                    st.error("Invalid ticker or no data available.")
                else:

                    # -------------------------
                    # Calculate Returns
                    # -------------------------
                    hist["returns"] = hist["Close"].pct_change()

                    volatility = hist["returns"].std() * np.sqrt(252)
                    mean_return = hist["returns"].mean() * 252

                    sharpe_ratio = mean_return / (volatility + 1e-6)

                    # -------------------------
                    # Normalize Metrics (0-1 Scale)
                    # -------------------------
                    vol_score = 1 / (1 + volatility * 8)

                    return_score = (mean_return + 0.2) / 0.4
                    return_score = np.clip(return_score, 0, 1)

                    sharpe_score = (sharpe_ratio + 2) / 4
                    sharpe_score = np.clip(sharpe_score, 0, 1)

                    # -------------------------
                    # ESG Proxy Score
                    # -------------------------
                    esg_score = (
                        vol_score * 35 +
                        return_score * 30 +
                        sharpe_score * 35
                    )

                    esg_score = np.clip(esg_score, 0, 100)

                    st.subheader(f"📊 ESG Proxy Score: {round(esg_score,2)} / 100")

                    # -------------------------
                    # Consequence Analysis
                    # -------------------------

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

                    st.markdown("### 📉 Impact Analysis")
                    st.write(f"Financial Risk Level: {risk}")
                    st.write(f"Investor Confidence: {investor_confidence}")
                    st.write(f"Regulatory Exposure: {regulatory_pressure}")

                    # -------------------------
                    # AI Insight Report
                    # -------------------------

                    st.markdown("### 🤖 AI Sustainability Insight")

                    insight = f"""
                    Based on 1-year market behavior, {company} demonstrates:

                    • Annual Volatility: {round(volatility,3)}
                    • Annual Return: {round(mean_return*100,2)}%
                    • Sharpe Ratio: {round(sharpe_ratio,2)}

                    The ESG proxy score of {round(esg_score,2)} reflects
                    market stability, risk-adjusted returns, and financial resilience.

                    Lower volatility and higher Sharpe ratio suggest
                    stronger governance discipline and sustainable growth signals.
                    """

                    st.write(insight)

                    # -------------------------
                    # Show Price Chart
                    # -------------------------

                    st.markdown("### 📈 1-Year Stock Price Trend")
                    st.line_chart(hist["Close"])

            except Exception:
                st.error("Data fetch failed. Please try another ticker or try later.")
