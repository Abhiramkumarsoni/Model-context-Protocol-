import os
import json
import sqlite3
from typing import Optional, List
from contextlib import contextmanager

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

app = FastAPI(
    title="ExpenseTracker",
    description="A simple expense tracking API (FastAPI port of the FastMCP version).",
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# Database setup
# ---------------------------------------------------------------------------

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
        """)


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


@app.on_event("startup")
def on_startup():
    init_db()


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class ExpenseCreate(BaseModel):
    date: str = Field(..., description="Expense date, e.g. YYYY-MM-DD")
    amount: float = Field(..., description="Expense amount")
    category: str = Field(..., description="Expense category")
    subcategory: str = Field("", description="Optional subcategory")
    note: str = Field("", description="Optional note")


class ExpenseOut(BaseModel):
    id: int
    date: str
    amount: float
    category: str
    subcategory: str
    note: str


class AddExpenseResponse(BaseModel):
    status: str
    id: int


class SummaryOut(BaseModel):
    category: str
    total_amount: float


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.post("/expenses", response_model=AddExpenseResponse)
def add_expense(expense: ExpenseCreate):
    """Add a new expense entry to the database."""
    with get_conn() as c:
        cur = c.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
            (expense.date, expense.amount, expense.category, expense.subcategory, expense.note),
        )
        c.commit()
        return {"status": "ok", "id": cur.lastrowid}


@app.get("/expenses", response_model=List[ExpenseOut])
def list_expenses(
    start_date: str = Query(..., description="Start date (inclusive), e.g. YYYY-MM-DD"),
    end_date: str = Query(..., description="End date (inclusive), e.g. YYYY-MM-DD"),
):
    """List expense entries within an inclusive date range."""
    with get_conn() as c:
        cur = c.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY id ASC
            """,
            (start_date, end_date),
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]


@app.get("/expenses/summary", response_model=List[SummaryOut])
def summarize(
    start_date: str = Query(..., description="Start date (inclusive), e.g. YYYY-MM-DD"),
    end_date: str = Query(..., description="End date (inclusive), e.g. YYYY-MM-DD"),
    category: Optional[str] = Query(None, description="Optional category filter"),
):
    """Summarize expenses by category within an inclusive date range."""
    with get_conn() as c:
        query = """
            SELECT category, SUM(amount) AS total_amount
            FROM expenses
            WHERE date BETWEEN ? AND ?
        """
        params = [start_date, end_date]

        if category:
            query += " AND category = ?"
            params.append(category)

        query += " GROUP BY category ORDER BY category ASC"

        cur = c.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]


@app.get("/categories")
def categories():
    """Return the contents of categories.json (read fresh on every call)."""
    if not os.path.exists(CATEGORIES_PATH):
        raise HTTPException(status_code=404, detail="categories.json not found")
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return JSONResponse(content=data)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


# cd "C:\MCP\server_with_fastapi"
# python -m uvicorn main:app --host 127.0.0.1 --port 8000

# then openn this in your browser:
# http://127.0.0.1:8000/
# http://127.0.0.1:8000/docs