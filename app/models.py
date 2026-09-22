from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


class IntakeRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Unstructured intake or client notes")


class ContactInfo(BaseModel):
    emails: list[str] = Field(default_factory=list)
    phone_numbers: list[str] = Field(default_factory=list)


class ActionItem(BaseModel):
    description: str
    priority: Literal["normal", "high"] = "normal"
    due_date: date | None = None


class ParsedWorkflow(BaseModel):
    contact: ContactInfo
    dates_mentioned: list[date]
    action_items: list[ActionItem]
    summary: str
