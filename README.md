**Live:** https://expense-tracker-o2mg.onrender.com/docs
# Expense Tracker API

A small REST API for tracking personal expenses, built with FastAPI and SQLite.
Log expenses, list them, fetch or delete one by id, and get spending totaled by category.

## Tech

- **FastAPI** — web framework / routing
- **SQLite** — file-based database (data persists to `expenses.db`)
- **Pydantic** — request body validation

## Setup

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open the interactive API docs at http://127.0.0.1:8000/docs

## Endpoints

| Method | Path               | Description                          |
|--------|--------------------|--------------------------------------|
| GET    | `/expenses`        | List all expenses                    |
| GET    | `/expenses/{id}`   | Get a single expense by id           |
| POST   | `/expenses`        | Create an expense                    |
| DELETE | `/expenses/{id}`   | Delete an expense by id              |
| GET    | `/summary`         | Total amount spent per category      |

### Example: create an expense

`POST /expenses`

```json
{
  "amount": 250.0,
  "category": "food",
  "note": "groceries"
}
```

### Example: summary response

`GET /summary`

```json
[
  {"category": "food", "total": 250.0},
  {"category": "transport", "total": 80.0}
]
```

## Data model

Each expense is one row in the `expenses` table:

| Column   | Type    | Notes                  |
|----------|---------|------------------------|
| id       | INTEGER | primary key, auto      |
| amount   | REAL    | expense amount         |
| category | TEXT    | e.g. food, transport   |
| note     | TEXT    | free-text description  |
