import streamlit as st
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

st.set_page_config(page_title="AI ESG Performance Predictor", layout="centered")

# -----------------------------
# 1. Train Model on Synthetic Data
# -----------------------------
@st.cache_resource
def train_model():

    np.random.seed(42)

    # Synthetic ESG dataset (100 samples)
    data = pd.DataFrame({
        "carbon_emission": np.random.randint(10, 100, 100),
        "renewable_energy": np.random.randint(5, 90, 100),
        "board_diversity": np.random.randint(5, 60, 100),
        "employee_turnover": np.random.randint(5, 40, 100),
        "debt_ratio": np.random.uniform(0.1, 0.9, 100),
    })

    # ESG Score formula (synthetic logic)
    data["esg_score"] = (
        100
        - 0.4 * data["carbon_emission"]
        + 0.3 * data["renewable_energy"]
        + 0.2 * data["board_diversity"]
        - 0.3 * data["employee_turnover"]
        - 20 * data["debt_ratio"]
    )

    # Normalize between 0-100
    data["esg_score"] = np.clip(data["esg_score"], 0, 100)

    X = data.drop("esg_score", axis=1)
    y = data["esg_score"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

    model = Sequential()
    model.add(Dense(16, activation='relu', input_shape=(5,)))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1))

    model.compile(loss='mse', optimizer='adam')
    model.fit(X_train, y_train, epochs=150, verbose=0)

    return model, scaler


model, scaler = train_model()

# -----------------------------
# 2. UI
# -----------------------------
st.title("🌍 AI-Powered ESG Performance & Impact Analyzer")

st.subheader("Enter Company ESG Metrics")

carbon = st.slider("Carbon Emission Intensity", 0, 100, 50)
renewable = st.slider("Renewable Energy Usage (%)", 0, 100, 30)
diversity = st.slider("Board Diversity (%)", 0, 100, 25)
turnover = st.slider("Employee Turnover (%)", 0, 50, 15)
debt = st.slider("Debt Ratio", 0.0, 1.0, 0.5)

if st.button("Predict ESG Performance"):

    input_data = np.array([[carbon, renewable, diversity, turnover, debt]])
    input_scaled = scaler.transform(input_data)

    esg_score = model.predict(input_scaled)[0][0]
    esg_score = float(np.clip(esg_score, 0, 100))

    st.subheader(f"📊 Predicted ESG Score: {round(esg_score,2)} / 100")

    # -----------------------------
    # 3. Consequence Analysis
    # -----------------------------

    if esg_score >= 80:
        financial_risk = "Low"
        regulatory_risk = "Low"
        investor_confidence = "High"
        cost_of_capital = "Decreases by ~1-2%"
    elif esg_score >= 50:
        financial_risk = "Moderate"
        regulatory_risk = "Medium"
        investor_confidence = "Stable"
        cost_of_capital = "Neutral impact"
    else:
        financial_risk = "High"
        regulatory_risk = "High"
        investor_confidence = "Low"
        cost_of_capital = "Increases by ~2-4%"

    st.markdown("### 📉 Consequence Analysis")
    st.write(f"**Financial Risk:** {financial_risk}")
    st.write(f"**Regulatory Exposure:** {regulatory_risk}")
    st.write(f"**Investor Confidence:** {investor_confidence}")
    st.write(f"**Cost of Capital Impact:** {cost_of_capital}")

    # -----------------------------
    # 4. AI-Style Report
    # -----------------------------

    st.markdown("### 🤖 AI Sustainability Report")

    report = f"""
    The company has an ESG performance score of {round(esg_score,2)}.

    Environmental analysis indicates carbon emission level at {carbon},
    with renewable adoption at {renewable}%.

    Governance strength is influenced by board diversity at {diversity}%
    and debt ratio of {round(debt,2)}.

    Social stability is reflected in employee turnover of {turnover}%.
    """

    if esg_score < 50:
        report += """
        The company faces significant sustainability challenges.
        High emissions and governance risk may lead to investor withdrawal
        and regulatory scrutiny. Immediate ESG reforms are recommended.
        """
    elif esg_score < 80:
        report += """
        The company demonstrates moderate ESG alignment.
        With strategic improvements in emissions and governance,
        long-term financial resilience can be enhanced.
        """
    else:
        report += """
        The company exhibits strong ESG leadership.
        Sustainable operations enhance investor confidence
        and reduce long-term financial risk.
        """

    st.write(report)
