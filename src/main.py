"""Entrypoint for the Smart Expense Tracker API.

Run with:  uvicorn src.main:app --reload
Docs at:   http://127.0.0.1:8000/docs
"""

from fastapi import FastAPI

from .routes import router

app = FastAPI(
    title="Smart Expense Tracker API",
    description="A small REST API to add, view, filter, total, and delete personal expenses.",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
def root() -> dict:
    return {"message": "Smart Expense Tracker API is running. See /docs for interactive API docs."}
