import streamlit as st
from add_update_ui import add_update_tab
from analytics_by_category import analytics_by_category_tab
from analytics_by_month import analytics_months_tab
from saved_expense_ui import saved_expense_tab
from expense_breakdown_ui import expense_breakdown_tab

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# Sidebar navigation
st.sidebar.title("💼 Expense Tracker")
page = st.sidebar.radio(
    label="Select Item",
    options=["Add/Update + Analytics", "Expense Breakdown", "Saved Expenses"],
    index=0
)

# Conditional rendering based on sidebar selection
if page == "Add/Update + Analytics":
    st.title("💰 Expense Management System")
    tab1, tab2, tab3 = st.tabs(["➕ Add / Update Expenses", "📊 Analytics by Category", "📅 Analytics by Month"])
    with tab1:
        add_update_tab()
    with tab2:
        analytics_by_category_tab()
    with tab3:
        analytics_months_tab()

elif page == "Saved Expenses":
    saved_expense_tab()  # a function that renders Saved Expenses page

elif page == "Expense Breakdown":
    expense_breakdown_tab()  # a function that renders Expense Breakdown page