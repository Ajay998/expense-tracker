from fastapi import FastAPI, HTTPException
from datetime import datetime
from backend.db_helper import fetch_expenses_for_date
app = FastAPI()

@app.get("/expenses/{expense_date}")
def get_expenses(expense_date: str):
    try:
        datetime.strptime(expense_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
    expenses = fetch_expenses_for_date(expense_date)
    if not expenses:
        raise HTTPException(status_code=404, detail="No expenses found for this date.")
    return {"date": expense_date, "expenses": expenses}
