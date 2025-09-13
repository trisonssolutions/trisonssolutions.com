import streamlit as st
import pandas as pd
import numpy as np
from prophet import Prophet
import plotly.graph_objects as go
from datetime import datetime, timedelta

# -------------------------------
# Page Setup
# -------------------------------
st.set_page_config(
    page_title="Financial Forecasting Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Financial Forecasting Dashboard")
st.markdown("Forecasting revenue trends using **Facebook Prophet**.")

# -------------------------------
# Example Data (Simulated)
# -------------------------------
@st.cache_data
def generate_sample_data():
    dates = pd.date_range(start="2022-01-01", end=datetime.today(), freq="W")
    np.random.seed(42)
    revenue = 1000 + np.cumsum(np.random.normal(0, 20, len(dates)))
    df = pd.DataFrame({"ds": dates, "y": revenue})
    return df

df = generate_sample_data()

# -------------------------------
# User Controls
# -------------------------------
st.sidebar.header("Forecast Settings")
periods = st.sidebar.slider("Forecast Horizon (weeks)", 4, 52, 26)
seasonality = st.sidebar.selectbox("Seasonality Mode", ["additive", "multiplicative"])

# -------------------------------
# Prophet Forecasting
# -------------------------------
m = Prophet(seasonality_mode=seasonality)
m.fit(df)

future = m.make_future_dataframe(periods=periods, freq="W")
forecast = m.predict(future)

# -------------------------------
# Visualization
# -------------------------------
fig = go.Figure()

# Actual data
fig.add_trace(go.Scatter(
    x=df["ds"], y=df["y"], mode="lines", name="Actual",
    line=dict(color="blue")
))

# Forecast line
fig.add_trace(go.Scatter(
    x=forecast["ds"], y=forecast["yhat"], mode="lines", name="Forecast",
    line=dict(color="orange")
))

# Confidence interval
fig.add_trace(go.Scatter(
    x=forecast["ds"], y=forecast["yhat_upper"], mode="lines",
    line=dict(width=0), showlegend=False
))
fig.add_trace(go.Scatter(
    x=forecast["ds"], y=forecast["yhat_lower"], mode="lines",
    line=dict(width=0), fill="tonexty", fillcolor="rgba(255,165,0,0.2)",
    name="Confidence Interval"
))

fig.update_layout(
    title="Revenue Forecast",
    xaxis_title="Date",
    yaxis_title="Revenue ($)",
    template="plotly_white",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# Show Forecast Data
# -------------------------------
with st.expander("🔎 View Forecast Data Table"):
    st.dataframe(forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(periods))
