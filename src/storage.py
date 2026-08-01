"""Simple JSON-file storage layer for expenses.

No database is used, per the assignment spec. All reads/writes go through
this module so the rest of the app never touches the file directly.
"""

import json
import threading
from pathlib import Path
from typing import List, Optional

from .models import Expense, ExpenseCreate

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_FILE = DATA_DIR / "expenses.json"

# Guards read-modify-write sequences so concurrent requests can't corrupt the file.
_lock = threading.Lock()


def _ensure_data_file() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]", encoding="utf-8")


def _read_all() -> List[dict]:
    _ensure_data_file()
    with DATA_FILE.open("r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _write_all(items: List[dict]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, default=str)


def get_all_expenses() -> List[Expense]:
    with _lock:
        raw = _read_all()
    return [Expense(**item) for item in raw]


def get_expenses_by_category(category: str) -> List[Expense]:
    return [e for e in get_all_expenses() if e.category.lower() == category.lower()]


def add_expense(expense_in: ExpenseCreate) -> Expense:
    with _lock:
        raw = _read_all()
        next_id = max((item["id"] for item in raw), default=0) + 1
        new_expense = Expense(id=next_id, **expense_in.model_dump())
        raw.append(json.loads(new_expense.model_dump_json()))
        _write_all(raw)
    return new_expense


def delete_expense(expense_id: int) -> bool:
    with _lock:
        raw = _read_all()
        filtered = [item for item in raw if item["id"] != expense_id]
        if len(filtered) == len(raw):
            return False
        _write_all(filtered)
    return True


def get_total(category: Optional[str] = None) -> float:
    expenses = get_all_expenses()
    if category:
        expenses = [e for e in expenses if e.category.lower() == category.lower()]
    return round(sum(e.amount for e in expenses), 2)
