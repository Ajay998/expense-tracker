import streamlit as st
import requests
from datetime import datetime
import pandas as pd

API_URL = "http://localhost:8000"

def saved_expense_tab():
    st.set_page_config(
        page_title="Saved Expenses",
        page_icon="💾",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    # Header
    st.markdown(
        "<h2 style='text-align:center; color:#10b981;'>💾 Saved Expenses</h2>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<p style='text-align:center; color:#9ca3af;'>View your saved expenses by date with a clean and professional table.</p>",
        unsafe_allow_html=True
    )
    st.markdown("---")

    # Sidebar: select date
    selected_date = st.sidebar.date_input("📅 Select Date", datetime(2024, 8, 1))

    # Fetch saved expenses
    try:
        response = requests.get(f"{API_URL}/expenses/{selected_date}")
        response.raise_for_status()
        expenses = response.json().get("expenses", [])
    except requests.RequestException:
        st.error("⚠️ Unable to fetch expenses. Please check your connection.")
        expenses = []

    if not expenses:
        st.info("No expenses found for this date.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(expenses)

    # Add total expenses
    total_expenses = df["amount"].sum()

    # Professional styled dataframe
    styled_df = df.style.set_properties(**{
        'background-color': '#111827',
        'color': '#f9fafb',
        'border-color': '#1f2937',
        'border-width': '1px',
        'border-style': 'solid',
        'padding': '6px',
        'font-size': '14px'
    }).set_table_styles([
        {'selector': 'th', 'props': [
            ('background-color', '#1f2937'),
            ('color', '#f9fafb'),
            ('font-size', '15px'),
            ('text-align', 'center'),
            ('padding', '8px')
        ]},
        {'selector': 'td', 'props': [('text-align', 'center')]}
    ])

    st.subheader(f"📋 Expenses for {selected_date.strftime('%d %b, %Y')}")
    st.dataframe(styled_df, use_container_width=True, height=400)

    st.markdown(
        f"<p style='text-align:right; color:#10b981; font-size:16px;'><b>Total Expenses: ₹{total_expenses:,.2f}</b></p>",
        unsafe_allow_html=True
    )

    # Summary by category
    st.subheader("📊 Summary by Category")
    category_totals = df.groupby("category")["amount"].sum().reset_index()
    category_totals.columns = ["Category", "Total Amount (₹)"]

    st.dataframe(category_totals.style.set_properties(**{
        'background-color': '#111827',
        'color': '#f9fafb',
        'border-color': '#1f2937',
        'border-width': '1px',
        'border-style': 'solid',
        'font-size': '14px',
        'text-align': 'center'
    }), use_container_width=True, height=300)