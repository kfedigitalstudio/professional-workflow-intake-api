import json
import re
from datetime import date, datetime

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
METADATA_LABEL_RE = re.compile(
    r"^\s*(?:client(?: email| phone)?|name|email|phone|telephone|hearing date|meeting date|date)\s*:",
    re.I,
)


def _dedupe(items):
    return list(dict.fromkeys(item.strip() for item in items if item.strip()))


def _extract_dates(text):
    found = []

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
            found.append(datetime.strptime(f"{month_name} {day} {year}", "%B %d %Y").date())
        except ValueError:
            pass

    return list(dict.fromkeys(found))


def _extract_actions(text):
    actions = []
    seen = set()

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or METADATA_LABEL_RE.match(line):
            continue

        if not (ACTION_PREFIX_RE.match(line) or ACTION_VERB_RE.search(line)):
            continue

        cleaned = ACTION_PREFIX_RE.sub("", line).strip(" -.;")
        if len(cleaned) < 4 or cleaned.lower() in seen:
            continue

        seen.add(cleaned.lower())
        dates = _extract_dates(cleaned)
        actions.append(
            {
                "description": cleaned,
                "priority": "high" if HIGH_PRIORITY_RE.search(cleaned) else "normal",
                "due_date": dates[0].isoformat() if dates else None,
            }
        )

    return actions


def parse_workflow(text):
    actions = _extract_actions(text)
    dates = _extract_dates(text)
    compact = " ".join(text.split())
    if len(compact) > 180:
        compact = compact[:177].rstrip() + "..."

    suffix = (
        f"{len(actions)} action item(s) identified."
        if actions
        else "No explicit action items identified."
    )

    return {
        "contact": {
            "emails": _dedupe(EMAIL_RE.findall(text)),
            "phone_numbers": _dedupe(PHONE_RE.findall(text)),
        },
        "dates_mentioned": [item.isoformat() for item in dates],
        "action_items": actions,
        "summary": f"{compact} | {suffix}",
    }


def parse_workflow_json(text):
    return json.dumps(parse_workflow(text))
