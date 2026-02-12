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
        with st.spinner("Fetching real-time financial data..."):

            stock = yf.Ticker(company)
            info = stock.info
            hist = stock.history(period="1y")

            if hist.empty:
                st.error("Invalid ticker or no data available.")
            else:

                # -------------------------
                # Financial Metrics
                # -------------------------

                market_cap = info.get("marketCap", 0)
                debt = info.get("totalDebt", 0)
                revenue = info.get("totalRevenue", 0)
                net_income = info.get("netIncomeToCommon", 0)

                # Volatility calculation
                hist["returns"] = hist["Close"].pct_change()
                volatility = hist["returns"].std() * np.sqrt(252)

                # Profit Margin
                if revenue != 0:
                    profit_margin = net_income / revenue
                else:
                    profit_margin = 0

                # Debt Ratio
                if market_cap != 0:
                    debt_ratio = debt / market_cap
                else:
                    debt_ratio = 0

                # -------------------------
                # ESG Proxy Score Calculation
                # -------------------------

                esg_score = (
                    (1 - volatility) * 30 +
                    (1 - debt_ratio) * 25 +
                    (profit_margin) * 25 +
                    (np.log1p(market_cap) / 30) * 20
                )

                esg_score = np.clip(esg_score * 10, 0, 100)

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
                Based on real-time market signals, {company} shows an ESG proxy score of {round(esg_score,2)}.

                Market volatility level: {round(volatility,3)}.
                Debt ratio: {round(debt_ratio,3)}.
                Profit margin: {round(profit_margin,3)}.

                Higher volatility and leverage increase governance and environmental risk signals.
                Stable profitability and strong market capitalization improve ESG stability outlook.
                """

                st.write(insight)
