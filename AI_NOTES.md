# AI Notes

## 1. Which parts were AI-generated vs. written by me

I used Claude to generate the initial scaffold for this project: `src/models.py`,
`src/storage.py`, `src/routes.py`, `src/main.py`, and the test suite in
`tests/test_api.py`. The overall design decisions were mine — using FastAPI with
JSON-file storage, splitting storage/routes/models into separate files, and the
specific set of endpoints required by the assignment (add, view all, filter by
category, total overall/by category, delete).

[EDIT THIS: note anything you personally rewrote, renamed, restructured, or added
after generation — e.g. if you changed error handling, added a new field, adjusted
naming conventions, etc.]

## 2. What I validated, tested, or changed in the AI's output, and why

- Ran `pytest` locally and confirmed all tests pass against a clean checkout.
- Ran the server with `uvicorn src.main:app --reload` and manually exercised every
  endpoint through `/docs` (Swagger UI) to confirm request/response shapes match
  the spec.
- Checked that amount validation actually rejects zero/negative values (422).
- Checked that category filtering is case-insensitive as intended.
- Confirmed deleting a non-existent id returns 404 rather than silently succeeding.

[EDIT THIS: replace with what you actually ran and checked. If you found a bug or
edge case the generated code missed, describe it and how you fixed it.]

## 3. Any AI suggestion I decided not to use, and why

[EDIT THIS: e.g. "Claude suggested adding a database option but the assignment
explicitly said no database is required, so I kept in-memory/JSON storage" — or
any other AI suggestion (bonus features, extra libraries, alternate structure)
you deliberately skipped, and your reasoning.]

---
**Before submitting:** replace the bracketed notes above with your own honest
account. The reviewers are explicitly checking that this reflects real usage and
testing, not a generic description — run the server and tests yourself first.
