from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.models import IntakeRequest, ParsedWorkflow
from app.services.parser import parse_workflow

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(
    title="Professional Workflow Intake API",
    version="1.1.0",
    description=(
        "Transforms unstructured professional-service intake notes into structured "
        "contacts, dates, and action items."
    ),
)

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def home() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/parse", response_model=ParsedWorkflow)
def parse_intake(request: IntakeRequest) -> ParsedWorkflow:
    return parse_workflow(request.text)
