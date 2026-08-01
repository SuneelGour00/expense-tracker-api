"""HTTP routes for the Smart Expense Tracker API."""

from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from . import storage
from .models import Expense, ExpenseCreate

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("", response_model=Expense, status_code=201)
def create_expense(expense: ExpenseCreate) -> Expense:
    """Add a new expense."""
    return storage.add_expense(expense)


@router.get("", response_model=List[Expense])
def list_expenses(
    category: Optional[str] = Query(None, description="Filter results by category"),
) -> List[Expense]:
    """View all expenses, or filter by category via ?category=Food"""
    if category:
        return storage.get_expenses_by_category(category)
    return storage.get_all_expenses()


@router.get("/total")
def total_expenses(
    category: Optional[str] = Query(None, description="Limit the total to one category"),
) -> dict:
    """Overall total, or total for a single category via ?category=Food"""
    return {"category": category, "total": storage.get_total(category)}


@router.delete("/{expense_id}", status_code=204)
def remove_expense(expense_id: int) -> None:
    """Delete an expense by id."""
    deleted = storage.delete_expense(expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Expense {expense_id} not found")
