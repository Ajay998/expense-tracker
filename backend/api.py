from fastapi import FastAPI, HTTPException
from datetime import date
from typing import List
from pydantic import BaseModel
from backend.db_helper import fetch_expenses_for_date, insert_expense, delete_expenses_for_date ,fetch_expense_summary
app = FastAPI()

class Expense(BaseModel):
    amount: float   
    category: str
    notes: str

class DateRange(BaseModel):
    start_date: date
    end_date: date


@app.get("/expenses/{expense_date}")
def get_expenses(expense_date: date):
    expenses = fetch_expenses_for_date(expense_date)
    if not expenses:
        raise HTTPException(status_code=404, detail="No expenses found for this date.")
    return {"date": expense_date, "expenses": expenses}

@app.post("/expenses/{expense_date}")
def add_or_update_expense(expense_date: date, expenses: List[Expense]):
    # delete_expenses_for_date(expense_date)
    for expense in expenses:
        insert_expense(expense_date, expense.amount, expense.category, expense.notes)
    return {"message": "Expenses added/updated successfully."}

@app.post("/analytics")
def get_analytics(date_range: DateRange):
    data = fetch_expense_summary(date_range.start_date, date_range.end_date)
    if data is None:
        raise HTTPException(status_code=404, detail="No data found for the given date range.")
    total = sum(item['total'] for item in data)
    breakdown = {}
    for row in data:
        percentage = (row['total']/total)*100 if total != 0 else 0
        breakdown[row['category']] = {
            "total": row['total'],
            "percentage": percentage
        }

    return breakdown