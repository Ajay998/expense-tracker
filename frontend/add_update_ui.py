import streamlit as st
import requests
from datetime import datetime

API_URL = "http://localhost:8000"  # adjust if needed


def add_update_tab():
    st.subheader("💰 Manage Your Expenses")

    # Date picker
    selected_date = st.date_input("Enter Date", datetime(2024, 8, 1), label_visibility="collapsed")


    # Fetch existing expenses
    response = requests.get(f"{API_URL}/expenses/{selected_date}")
    if response.status_code == 200:
        existing_expenses = response.json().get("expenses", [])
    else:
        st.error("⚠️ Could not fetch expenses for this date.")
        existing_expenses = []

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    with st.form(key="expense_form"):
        st.markdown("### 📝 Enter Expenses")

        # Table-like header row
        col1, col2, col3 = st.columns([2, 2, 4])
        with col1:
            st.markdown("**Amount (₹)**")
        with col2:
            st.markdown("**Category**")
        with col3:
            st.markdown("**Notes**")

        expenses = []
        for i in range(5):
            if i < len(existing_expenses):
                amount = existing_expenses[i]["amount"]
                category = existing_expenses[i]["category"]
                notes = existing_expenses[i]["notes"]
            else:
                amount, category, notes = 0.0, "Shopping", ""

            col1, col2, col3 = st.columns([2, 2, 4])
            with col1:
                amount_input = st.number_input(
                    label="Amount",
                    min_value=0.0,
                    step=10.0,
                    value=float(amount),
                    key=f"amount_{i}",
                    label_visibility="collapsed",
                )
            with col2:
                category_input = st.selectbox(
                    label="Category",
                    options=categories,
                    index=categories.index(category),
                    key=f"category_{i}",
                    label_visibility="collapsed",
                )
            with col3:
                notes_input = st.text_input(
                    label="Notes",
                    value=notes,
                    key=f"notes_{i}",
                    placeholder="Optional notes...",
                    label_visibility="collapsed",
                )

            expenses.append(
                {"amount": amount_input, "category": category_input, "notes": notes_input}
            )

        st.markdown("---")
        submit_button = st.form_submit_button("💾 Save Expenses")

        if submit_button:
            filtered_expenses = [e for e in expenses if e["amount"] > 0]

            if not filtered_expenses:
                st.warning("⚠️ Please enter at least one expense before saving.")
            else:
                response = requests.post(
                    f"{API_URL}/expenses/{selected_date}", json=filtered_expenses
                )
                if response.status_code == 200:
                    st.success("✅ Expenses updated successfully!")
                else:
                    st.error("❌ Failed to update expenses.")