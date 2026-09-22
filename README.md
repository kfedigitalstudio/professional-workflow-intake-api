# Professional Workflow Intake API

A small Python/FastAPI service that converts unstructured professional-service intake notes into structured, reusable workflow data.

## Why this project

Many professional workflows begin as emails, call notes, or free-form intake text. This API turns that unstructured text into a predictable JSON structure containing:

- email addresses and phone numbers
- dates and deadlines
- action items
- task priority
- a concise intake summary

The project is intentionally deterministic and dependency-light. It demonstrates workflow analysis, REST API design, validation, testing, and containerization without requiring a paid AI service.

## Tech stack

- Python 3.12
- FastAPI
- Pydantic
- Pytest
- REST/JSON
- Docker

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API documentation.

## Example request

```bash
curl -X POST http://127.0.0.1:8000/parse \
  -H "Content-Type: application/json" \
  -d @sample_request.json
```

## Example output

```json
{
  "contact": {
    "emails": ["jordan.lee@example.com"],
    "phone_numbers": ["(317) 555-0199"]
  },
  "dates_mentioned": ["2026-10-15", "2026-10-10"],
  "action_items": [
    {
      "description": "Review documents by 10/10/2026",
      "priority": "normal",
      "due_date": "2026-10-10"
    },
    {
      "description": "URGENT: email client today to confirm missing records",
      "priority": "high",
      "due_date": null
    }
  ],
  "summary": "..."
}
```

## Tests

```bash
pytest -q
```

## Possible next steps

- add SQLite/PostgreSQL persistence
- add authentication and role-based access
- add configurable workflow rules
- add optional LLM-assisted classification behind a provider interface
- add webhook integrations for downstream workflow tools
