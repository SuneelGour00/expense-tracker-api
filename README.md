# expense-tracker-api
Smart Expense Tracker API
A REST API for managing personal expenses, built with Python + FastAPI.
Data is stored in a local JSON file (`data/expenses.json`) — no database required.
What it does
`POST   /expenses`        — add an expense (title, amount, category, date)
`GET    /expenses`        — view all expenses
`GET    /expenses?category=Food` — filter expenses by category
`GET    /expenses/total`  — total of all expenses
`GET    /expenses/total?category=Food` — total for one category
`DELETE /expenses/{id}`   — delete an expense by id
Interactive Swagger docs are auto-generated at `/docs` once the server is running.
Project structure
```
expense-tracker/
  data/
    expenses.json     # persisted expenses (JSON array)
  src/
    main.py           # FastAPI app entrypoint
    models.py         # Pydantic request/response models
    routes.py          # API endpoints
    storage.py         # JSON file read/write logic
  tests/
    test_api.py        # pytest test suite
  AI_NOTES.md
  README.md
  requirements.txt
```
How to install
From the `expense-tracker/` project root:
```bash
python -m venv venv
```
Activate the virtual environment:
Windows (PowerShell): `venv\Scripts\Activate.ps1`
macOS / Linux: `source venv/bin/activate`
Install dependencies:
```bash
pip install -r requirements.txt
```
How to run the server
```bash
uvicorn src.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.
Open `http://127.0.0.1:8000/docs` for interactive Swagger UI where you can try every endpoint.
How to run the tests
```bash
pytest
```
Tests use FastAPI's `TestClient` and run against a temporary JSON file (via a pytest fixture),
so they never touch or overwrite your real `data/expenses.json`.
Example usage (curl)
```bash
# Add an expense
curl -X POST http://127.0.0.1:8000/expenses \
  -H "Content-Type: application/json" \
  -d '{"title": "Groceries", "amount": 45.20, "category": "Food", "date": "2026-07-30"}'

# View all expenses
curl http://127.0.0.1:8000/expenses

# Filter by category
curl "http://127.0.0.1:8000/expenses?category=Food"

# Total (overall and by category)
curl http://127.0.0.1:8000/expenses/total
curl "http://127.0.0.1:8000/expenses/total?category=Food"

# Delete an expense
curl -X DELETE http://127.0.0.1:8000/expenses/1
```
Notes
Amounts must be greater than 0 (validated by Pydantic — invalid input returns `422`).
Category matching is case-insensitive.
Expense IDs auto-increment based on the current highest ID in storage.
