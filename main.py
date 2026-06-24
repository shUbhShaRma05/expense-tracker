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
