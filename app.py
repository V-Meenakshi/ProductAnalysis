import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Title
st.title("🍫 Chocolate Sales Forecast Dashboard")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("Chocolate Sales.csv")
    df['Amount'] = df['Amount'].replace('[\$,]', '', regex=True).astype(float)
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    return df

df = load_data()

# Sidebar filters
product_list = df['Product'].unique().tolist()
selected_product = st.sidebar.selectbox("Select a Product", product_list)

# Line plot of sales trend
st.subheader(f"📈 Sales Trend for: {selected_product}")
product_df = df[df['Product'] == selected_product]
product_df = product_df.groupby('Date')['Amount'].sum().reset_index()

fig1 = px.line(product_df, x='Date', y='Amount', title=f"Weekly Sales for {selected_product}")
st.plotly_chart(fig1, use_container_width=True)

# Show forecast chart if available
try:
    forecast_df = pd.read_csv("forecast_next_4_weeks.csv")
    st.subheader("🔮 4-Week Forecast")

    row = forecast_df[forecast_df['Product'] == selected_product]
    if not row.empty:
        weeks = ['Week+1', 'Week+2', 'Week+3', 'Week+4']
        forecast_vals = row[weeks].values.flatten().astype(float)

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=weeks, y=forecast_vals, name='Forecasted Sales'))
        fig2.update_layout(title=f"Forecast for {selected_product}",
                           xaxis_title='Week', yaxis_title='Amount')
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("No forecast data available for this product.")
except Exception as e:
    st.warning("Forecast file not found. Upload 'forecast_next_4_weeks.csv'.")

# Optional: Display raw data
if st.checkbox("Show Raw Data"):
    st.write(df.head())
