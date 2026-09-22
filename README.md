# Professional Workflow Intake API

A Python/FastAPI portfolio project that converts unstructured professional-service intake notes into structured workflow data. The repository includes a REST API and a GitHub Pages demo that runs the parsing logic directly in the browser with Pyodide.

## Live demo

**GitHub Pages:** https://kfedigitalstudio.github.io/professional-workflow-intake-api/

The public demo runs Python in the visitor's browser. Intake text is processed locally and is not sent to a hosted backend service.

## What it does

Many professional workflows begin as emails, call notes, or free-form intake text. This project turns that unstructured text into a predictable structure containing:

- email addresses and phone numbers
- dates and deadlines
- action items
- task priority
- a concise intake summary

The parser is intentionally deterministic and dependency-light. It demonstrates Python application development, workflow analysis, REST API design, validation, testing, frontend/API integration, browser-based Python, and containerization without requiring a paid external service.

## Tech stack

- Python 3.12
- FastAPI
- Pydantic
- Pyodide / WebAssembly
- REST/JSON
- HTML, CSS, and JavaScript
- Pytest
- Docker
- GitHub Pages

## GitHub Pages demo

The `docs/` directory contains the static portfolio site. Pyodide loads a Python runtime in the browser, then executes `docs/parser.py` locally. JavaScript renders the resulting structured data in the interface.

The browser demo and the FastAPI service use the same extraction approach. The FastAPI implementation remains available under `app/` for local or server deployment.

To publish the demo with GitHub Pages, configure the repository to deploy from:

- Branch: `main`
- Folder: `/docs`

## Run the FastAPI version locally

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open:

- `http://127.0.0.1:8000/` — FastAPI-hosted portfolio interface
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

The FastAPI suite covers the parser, JSON API, portfolio homepage, and static asset delivery.

## Server deployment option

The FastAPI application can also be deployed as a conventional Python web service. A typical production start command is:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

The GitHub Pages demo does not require a Python server.

## Possible next steps

- add SQLite/PostgreSQL persistence to the server version
- add authentication and role-based access
- add configurable workflow rules
- add webhook integrations for downstream workflow tools
