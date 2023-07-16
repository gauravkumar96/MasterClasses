import os
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Stock Dashboard", page_icon=":chart_with_upwards_trend:", layout="wide")

# Load stock data from CSV files
@st.cache(allow_output_mutation=True)
def load_stock_data():
    folder_path = "equity_data"
    csv_files = [file for file in os.listdir(folder_path) if file.endswith(".csv")]
    data = {}

    for file in csv_files:
        stock_name = os.path.splitext(file)[0]  # Extract stock name from file name
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path, parse_dates=["date"],index_col=[0])
        # df = df.drop("Unnamed: 0", axis=1)  # Remove the "Unnamed: 0" column
        data[stock_name] = df

    return data

stock_data = load_stock_data()

# Sidebar filters
st.sidebar.header("Filters")
stock_name = st.sidebar.selectbox("Select Stock", options=list(stock_data.keys()))

# Apply filters
filtered_df = stock_data[stock_name]

# Main page content
st.title(f"Financial Dashboard - {stock_name}")
st.markdown("---")

# Display filtered data
st.subheader(f"Stock Data - {stock_name}")
st.dataframe(filtered_df)

# Line Chart: Stock Closing Price over Time
fig = go.Figure()
fig.add_trace(go.Scatter(x=filtered_df["date"], y=filtered_df["close"], name="Closing Price"))
fig.update_layout(title="Stock Closing Price over Time", xaxis_title="Date", yaxis_title="Price")
st.plotly_chart(fig)