import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://localhost:8000"

def analytics_months_tab():
    st.markdown("### 📅 Monthly Expense Summary")

    response = requests.get(f"{API_URL}/monthly_summary/")
    monthly_summary = response.json()

    df = pd.DataFrame(monthly_summary)
    df.rename(columns={
        "expense_month": "Month Number",
        "month_name": "Month Name",
        "total": "Total"
    }, inplace=True)

    df_sorted = df.sort_values(by="Month Number", ascending=False)

    fig = px.bar(df_sorted, x="Month Name", y="Total", color="Month Name",
                 title="Total Expenses by Month", text_auto='.2f')
    st.plotly_chart(fig, use_container_width=True)

    df_sorted["Total"] = df_sorted["Total"].map("{:.2f}".format)
    st.dataframe(df_sorted[["Month Name", "Total"]], use_container_width=True)