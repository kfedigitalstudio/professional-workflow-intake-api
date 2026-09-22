import re
from datetime import date, datetime

from app.models import ActionItem, ContactInfo, ParsedWorkflow

EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
PHONE_RE = re.compile(r"(?<!\d)(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]\d{3}[-.\s]\d{4}(?!\d)")
ISO_DATE_RE = re.compile(r"\b(20\d{2}|19\d{2})-(\d{1,2})-(\d{1,2})\b")
US_DATE_RE = re.compile(r"\b(\d{1,2})/(\d{1,2})/(20\d{2}|19\d{2})\b")
MONTH_DATE_RE = re.compile(
    r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+"
    r"(\d{1,2})(?:st|nd|rd|th)?,?\s+(20\d{2}|19\d{2})\b",
    re.I,
)
ACTION_PREFIX_RE = re.compile(r"^\s*(?:[-*•]|\d+[.)]|todo:|action:|next step:)\s*", re.I)
ACTION_VERB_RE = re.compile(
    r"\b(call|email|contact|send|submit|file|review|prepare|schedule|follow up|follow-up|upload|collect|verify|confirm|draft|update|request)\b",
    re.I,
)
HIGH_PRIORITY_RE = re.compile(r"\b(urgent|asap|immediately|high priority|today)\b", re.I)
METADATA_LABEL_RE = re.compile(r"^\s*(?:client(?: email| phone)?|name|email|phone|telephone|hearing date|meeting date|date)\s*:", re.I)


def _dedupe(items: list[str]) -> list[str]:
    return list(dict.fromkeys(item.strip() for item in items if item.strip()))


def _extract_dates(text: str) -> list[date]:
    found: list[date] = []

    for year, month, day in ISO_DATE_RE.findall(text):
        try:
            found.append(date(int(year), int(month), int(day)))
        except ValueError:
            pass

    for month, day, year in US_DATE_RE.findall(text):
        try:
            found.append(date(int(year), int(month), int(day)))
        except ValueError:
            pass

    for month_name, day, year in MONTH_DATE_RE.findall(text):
        try:
            parsed = datetime.strptime(f"{month_name} {day} {year}", "%B %d %Y").date()
            found.append(parsed)
        except ValueError:
            pass

    return list(dict.fromkeys(found))


def _line_due_date(line: str) -> date | None:
    dates = _extract_dates(line)
    return dates[0] if dates else None


def _extract_actions(text: str) -> list[ActionItem]:
    actions: list[ActionItem] = []
    seen: set[str] = set()

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        if METADATA_LABEL_RE.match(line):
            continue

        has_prefix = bool(ACTION_PREFIX_RE.match(line))
        has_action_verb = bool(ACTION_VERB_RE.search(line))
        if not (has_prefix or has_action_verb):
            continue

        cleaned = ACTION_PREFIX_RE.sub("", line).strip(" -.;")
        if len(cleaned) < 4:
            continue

        key = cleaned.lower()
        if key in seen:
            continue
        seen.add(key)

        priority = "high" if HIGH_PRIORITY_RE.search(cleaned) else "normal"
        actions.append(
            ActionItem(
                description=cleaned,
                priority=priority,
                due_date=_line_due_date(cleaned),
            )
        )

    return actions


def _make_summary(text: str, action_count: int) -> str:
    compact = " ".join(text.split())
    if len(compact) > 180:
        compact = compact[:177].rstrip() + "..."
    if action_count:
        return f"{compact} | {action_count} action item(s) identified."
    return f"{compact} | No explicit action items identified."


def parse_workflow(text: str) -> ParsedWorkflow:
    emails = _dedupe(EMAIL_RE.findall(text))
    phones = _dedupe(PHONE_RE.findall(text))
    dates = _extract_dates(text)
    actions = _extract_actions(text)

    return ParsedWorkflow(
        contact=ContactInfo(emails=emails, phone_numbers=phones),
        dates_mentioned=dates,
        action_items=actions,
        summary=_make_summary(text, len(actions)),
    )
