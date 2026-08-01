"""Pydantic models used to validate and serialize expenses."""

from datetime import date as date_type

from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    """Fields required to create a new expense (id is assigned by the server)."""

    title: str = Field(..., min_length=1, description="Short description of the expense")
    amount: float = Field(..., gt=0, description="Expense amount, must be greater than 0")
    category: str = Field(..., min_length=1, description="Category, e.g. Food, Travel, Rent")
    date: date_type = Field(..., description="Date the expense occurred (YYYY-MM-DD)")


class Expense(ExpenseCreate):
    """A fully stored expense, including its server-assigned id."""

    id: int
