import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

API_URL = "http://localhost:8000"

def expense_breakdown_tab():
    st.set_page_config(page_title="Expense Breakdown", page_icon="📈", layout="wide")

    st.title("📈 Expense Breakdown")
    st.markdown("Analyze your spending with professional, interactive charts and tables.")

    # Sidebar Controls
    with st.sidebar:
        st.header("⚙️ Controls")

        selected_date = st.date_input("📅 Select Date", datetime(2024, 8, 1))

        # Visualization type
        chart_types = st.multiselect(
            "📊 Select Visualization Type",
            ["Pie Chart", "Bar Chart", "Line Chart"],
            default=["Pie Chart", "Bar Chart"]
        )

        # Download options
        st.markdown("### 📥 Download Data")
        download_format = st.radio("Choose format", ["CSV", "Excel"])
    
    # Fetch expenses
    try:
        response = requests.get(f"{API_URL}/expenses/{selected_date}")
        response.raise_for_status()
        expenses = response.json().get("expenses", [])
    except:
        expenses = []

    if not expenses:
        st.info("No expenses found for this date.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(expenses)

    # Show DataFrame
    st.subheader(f"💾 Expenses on {selected_date.strftime('%d %b %Y')}")
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Prepare category totals
    category_totals = df.groupby("category")["amount"].sum().reset_index()

    # Layout for charts
    st.markdown("### 📊 Visualizations")
    cols = st.columns(len(chart_types))

    for i, chart in enumerate(chart_types):
        with cols[i]:
            if chart == "Pie Chart":
                fig, ax = plt.subplots(figsize=(3, 3))
                ax.pie(category_totals["amount"], labels=category_totals["category"], autopct="%1.1f%%")
                ax.set_title("Expense Distribution (Pie)")
                st.pyplot(fig)

            elif chart == "Bar Chart":
                st.bar_chart(category_totals.set_index("category"))

            elif chart == "Line Chart":
                st.line_chart(category_totals.set_index("category"))

    # Download Data
    if download_format == "CSV":
        st.download_button(
            label="⬇️ Download CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name=f"expenses_{selected_date}.csv",
            mime="text/csv"
        )
    else:
        from io import BytesIO
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Expenses")
        st.download_button(
            label="⬇️ Download Excel",
            data=output.getvalue(),
            file_name=f"expenses_{selected_date}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )