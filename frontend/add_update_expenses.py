import streamlit as st
import requests
from datetime import datetime

API_URL = "http://localhost:8000"  # Update to production URL if needed
CATEGORIES = ["Rent", "Food", "Shopping", "Entertainment", "Other"]
MAX_ENTRIES = 5

def fetch_expenses(date):
    """Fetch expenses from API."""
    try:
        response = requests.get(f"{API_URL}/expenses/{date}")
        response.raise_for_status()
        return response.json().get("expenses", [])
    except requests.RequestException:
        st.error("⚠️ Unable to fetch expenses. Please check your connection.")
        return []

def save_expenses(date, expenses):
    """Save expenses to API."""
    try:
        response = requests.post(f"{API_URL}/expenses/{date}", json=expenses)
        if response.status_code == 200:
            st.success("✅ Expenses saved successfully!")
        else:
            st.error("❌ Failed to save expenses. Please try again.")
    except requests.RequestException:
        st.error("❌ Network error while saving expenses.")

def add_update_tab():
    st.markdown(
        """
        Easily manage your daily expenses.  
        Select a date, add or update entries, and stay on top of your budget.
        """,
        help="Use this tool to record and review your daily spending."
    )

    selected_date = st.date_input(
        "📅 Select Date",
        datetime(2024, 8, 1),
        help="Choose the date for which you want to manage expenses.",
        key="expense_date_input"
    )

    existing_expenses = fetch_expenses(selected_date)

    with st.expander("📝 Add or Update Expenses", expanded=True):
        with st.form(key="expense_form"):
            expenses = []
            for i in range(MAX_ENTRIES):
                amount = existing_expenses[i]["amount"] if i < len(existing_expenses) else 0.0
                category = existing_expenses[i]["category"] if i < len(existing_expenses) else "Shopping"
                notes = existing_expenses[i]["notes"] if i < len(existing_expenses) else ""

                col1, col2, col3 = st.columns([2, 2, 4])
                amount_input = col1.number_input(
                    "Amount (₹)",
                    min_value=0.0,
                    step=10.0,
                    value=float(amount),
                    key=f"amount_{i}",
                    help="Enter the amount spent"
                )
                category_input = col2.selectbox(
                    "Category",
                    options=CATEGORIES,
                    index=CATEGORIES.index(category),
                    key=f"category_{i}",
                    help="Select the expense category"
                )
                notes_input = col3.text_input(
                    "Notes",
                    value=notes,
                    key=f"notes_{i}",
                    placeholder="Optional notes...",
                    help="Add any relevant details"
                )

                expenses.append({
                    "amount": amount_input,
                    "category": category_input,
                    "notes": notes_input
                })

            st.markdown("---")
            if st.form_submit_button("💾 Save Expenses"):
                filtered = [e for e in expenses if e["amount"] > 0]
                if not filtered:
                    st.warning("⚠️ Please enter at least one expense before saving.")
                else:
                    save_expenses(selected_date, filtered)


    


