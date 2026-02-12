import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd

st.set_page_config(page_title="Real-Time ESG Proxy Analyzer", layout="centered")

st.title("🌍 Real-Time ESG Proxy Performance Analyzer")

company = st.text_input("Enter Company Ticker (e.g., RELIANCE.NS, TCS.NS, AAPL)")

if st.button("Analyze ESG Performance"):

    if company == "":
        st.warning("Please enter a company ticker.")
    else:
        with st.spinner("Fetching market data..."):

            try:
                stock = yf.Ticker(company)
                hist = stock.history(period="1y")

                if hist.empty:
                    st.error("Invalid ticker or no data available.")
                else:

                    # -------------------------
                    # Volatility
                    # -------------------------
                    hist["returns"] = hist["Close"].pct_change()
                    volatility = hist["returns"].std() * np.sqrt(252)

                    # -------------------------
                    # Price Growth
                    # -------------------------
                    start_price = hist["Close"].iloc[0]
                    end_price = hist["Close"].iloc[-1]
                    growth = (end_price - start_price) / start_price

                    # -------------------------
                    # Stability Score
                    # -------------------------
                    stability = 1 - volatility

                    # -------------------------
                    # ESG Proxy Score
                    # -------------------------
                    esg_score = (
                        stability * 40 +
                        growth * 30 +
                        (1 - volatility) * 30
                    )

                    esg_score = np.clip(esg_score * 100, 0, 100)

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
                    # AI Insight
                    # -------------------------

                    st.markdown("### 🤖 AI Sustainability Insight")

                    insight = f"""
                    Based on 1-year market behavior, {company} shows an ESG proxy score of {round(esg_score,2)}.

                    Annual volatility: {round(volatility,3)}.
                    Price growth over 1 year: {round(growth*100,2)}%.

                    Lower volatility and consistent price growth
                    indicate stronger governance stability and
                    lower sustainability-related risk exposure.
                    """

                    st.write(insight)

            except Exception:
                st.error("Data fetch failed. Please try again later.")
