import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import plotly.express as px

# API endpoint
API_URL = "http://localhost:8000"

def analytics_by_category_tab():
    # Set the page title and layout
    st.set_page_config(page_title="Expense Analytics", layout="wide")
    
    # Display a header
    st.markdown("# 📊 Expense Analytics by Category")
    st.markdown("Analyze your expenses by category over a specified date range.")

    # Date input controls with improved spacing
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 8, 1))
    with col2:
        end_date = st.date_input("End Date", datetime(2024, 8, 5))

    # Button to trigger analytics generation
    if st.button("📈 Generate Analytics"):
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }

        # Fetch data from the API
        try:
            response = requests.post(f"{API_URL}/analytics/", json=payload)
            response.raise_for_status()  # Raise error for bad responses
            response_data = response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching data: {e}")
            return

        # Prepare the data for display
        data = {
            "Category": list(response_data.keys()),
            "Total": [response_data[cat]["total"] for cat in response_data],
            "Percentage": [response_data[cat]["percentage"] for cat in response_data]
        }

        df = pd.DataFrame(data).sort_values(by="Percentage", ascending=False)

        # Plotly bar chart
        fig = px.bar(
            df, 
            x="Category", 
            y="Percentage", 
            color="Category", 
            title="Category-wise Expense Breakdown",
            text_auto='.2f', 
            labels={"Percentage": "Percentage (%)"},
            color_discrete_sequence=px.colors.qualitative.Set1  # Custom color palette
        )

        # Add chart with full container width
        st.plotly_chart(fig, use_container_width=True)

        # Format the table with readable values
        df["Total"] = df["Total"].map("${:.2f}".format)  # Format total as currency
        df["Percentage"] = df["Percentage"].map("{:.2f}%".format)  # Format percentage

        # Display the DataFrame with a professional look
        st.subheader("💼 Category Breakdown")
        st.dataframe(df, use_container_width=True, height=300)


