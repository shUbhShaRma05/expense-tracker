from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class Expense(BaseModel):
    amount: float
    category: str
    note: str

def get_db():
    conn = sqlite3.connect("expenses.db")
    conn.row_factory = sqlite3.Row
    return conn

conn = get_db()
conn.execute(
    "CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY, amount REAL, category TEXT, note TEXT)"
)
conn.commit()
conn.close()

@app.get("/")
def home():
    return {"app": "expense tracker"}

@app.post("/expenses")
def create_expense(expense:Expense):
    conn= get_db()
    conn.execute(
        "INSERT INTO expenses(amount,category,note) VALUES(?,?,?)",
        (expense.amount, expense.category,expense.note),
    )
    conn.commit()
    conn.close()
    return {
        "Saved": {"amount":expense.amount,"category":expense.category,"note":expense.note}
    }

@app.get("/expenses")
def list_expenses():
    conn = get_db()
    rows = conn.execute(
        "SELECT id,amount,category,note from expenses").fetchall()
    conn.close()
    return[dict(row) for row in rows]

@app.get("/expenses/{expense_id}")
def list_expense(expense_id:int):
    conn = get_db()
    row = conn.execute(
        "SELECT id,amount,category,note from expenses where id = ?",(expense_id,)
    ).fetchone()
    conn.close()
    return dict(row)


@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id:int):
    conn = get_db()
    conn.execute(
        "DELETE from expenses where id = ?",(expense_id,)
    )
    conn.commit()
    conn.close()
    return{"Deleted":expense_id}

@app.get("/summary")
def summary():
    conn = get_db()
    rows = conn.execute(
        "Select category, SUM(amount) AS total from expenses group by category"
    ).fetchall()
    conn.close()
    return[dict(row) for row in rows]