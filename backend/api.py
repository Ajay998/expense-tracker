from fastapi import FastAPI, HTTPException
from datetime import date, datetime
from typing import List
from pydantic import BaseModel
from backend.db_helper import fetch_expenses_for_date, insert_expense, delete_expenses_for_date
app = FastAPI()

class Expense(BaseModel):
    amount: float
    category: str
    notes: str


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

