from fastapi import FastAPI

from app.models import IntakeRequest, ParsedWorkflow
from app.services.parser import parse_workflow

app = FastAPI(
    title="Professional Workflow Intake API",
    version="1.0.0",
    description=(
        "Transforms unstructured professional-service intake notes into structured "
        "contacts, dates, and action items."
    ),
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/parse", response_model=ParsedWorkflow)
def parse_intake(request: IntakeRequest) -> ParsedWorkflow:
    return parse_workflow(request.text)
