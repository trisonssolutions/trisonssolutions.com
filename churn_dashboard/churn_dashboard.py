import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Telecom Churn Dashboard")

df = pd.DataFrame({
    "Customer": ["A","B","C","D"],
    "Churn Probability": [0.2, 0.8, 0.5, 0.1]
})

st.write("Churn Predictions")
st.dataframe(df)

fig = px.bar(df, x="Customer", y="Churn Probability", title="Customer Churn Risk")
st.plotly_chart(fig)
