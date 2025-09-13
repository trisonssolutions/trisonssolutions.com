import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -------------------------------
# Page Setup
# -------------------------------
st.set_page_config(
    page_title="Customer Churn Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Telecom Customer Churn Dashboard")
st.markdown("Analyze churn rates and customer retention trends.")

# -------------------------------
# Example Data (Simulated)
# -------------------------------
@st.cache_data
def load_sample_data():
    np.random.seed(42)
    n = 1000
    df = pd.DataFrame({
        "CustomerID": range(1, n + 1),
        "TenureMonths": np.random.randint(1, 60, n),
        "MonthlyCharges": np.random.randint(20, 120, n),
        "Contract": np.random.choice(["Month-to-Month", "One Year", "Two Year"], n, p=[0.6, 0.25, 0.15]),
        "Churn": np.random.choice(["Yes", "No"], n, p=[0.27, 0.73])
    })
    return df

df = load_sample_data()

# -------------------------------
# KPIs
# -------------------------------
total_customers = len(df)
churn_rate = (df["Churn"].value_counts(normalize=True)["Yes"]) * 100
avg_tenure = df["TenureMonths"].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Churn Rate", f"{churn_rate:.1f}%")
col3.metric("Avg. Tenure", f"{avg_tenure:.1f} months")

# -------------------------------
# Churn by Contract Type
# -------------------------------
contract_churn = df.groupby("Contract")["Churn"].value_counts(normalize=True).mul(100).rename("Percentage").reset_index()

fig1 = px.bar(
    contract_churn[contract_churn["Churn"] == "Yes"],
    x="Contract", y="Percentage",
    title="Churn % by Contract Type",
    color="Contract",
    text=contract_churn[contract_churn["Churn"] == "Yes"]["Percentage"].round(1).astype(str) + "%"
)
fig1.update_layout(yaxis_title="Churn %")
st.plotly_chart(fig1, use_container_width=True)

# -------------------------------
# Monthly Charges vs. Churn
# -------------------------------
fig2 = px.histogram(
    df, x="MonthlyCharges", color="Churn", barmode="overlay",
    title="Distribution of Monthly Charges by Churn Status",
    nbins=40
)
st.plotly_chart(fig2, use_container_width=True)

# -------------------------------
# Data Explorer
# -------------------------------
with st.expander("🔎 View Raw Data"):
    st.dataframe(df.head(50))
