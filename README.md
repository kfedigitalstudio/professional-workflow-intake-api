# Professional Workflow Intake API

A Python/FastAPI portfolio project that converts unstructured professional-service intake notes into structured workflow data. The repository includes both a REST API and a lightweight browser interface for demonstrating the workflow end to end.

## What it does

Many professional workflows begin as emails, call notes, or free-form intake text. This project turns that unstructured text into a predictable structure containing:

- email addresses and phone numbers
- dates and deadlines
- action items
- task priority
- a concise intake summary

The parser is intentionally deterministic and dependency-light. It demonstrates Python application development, workflow analysis, REST API design, validation, testing, frontend/API integration, and containerization without requiring a paid external service.

## Tech stack

- Python 3.12
- FastAPI
- Pydantic
- REST/JSON
- HTML, CSS, and JavaScript
- Pytest
- Docker

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open:

- `http://127.0.0.1:8000/` — portfolio web interface
- `http://127.0.0.1:8000/docs` — interactive API documentation
- `http://127.0.0.1:8000/health` — health check

## Example API request

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

The suite covers the parser, JSON API, portfolio homepage, and static asset delivery.

## Deployment

The application is deployment-ready as a single FastAPI service. A typical production start command is:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Possible next steps

- add SQLite/PostgreSQL persistence
- add authentication and role-based access
- add configurable workflow rules
- add webhook integrations for downstream workflow tools
