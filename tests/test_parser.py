from datetime import date

from app.services.parser import parse_workflow


def test_extracts_contact_dates_and_actions() -> None:
    text = """
    Client: Jordan Lee
    Email: jordan.lee@example.com
    Phone: (317) 555-0199
    Hearing date: October 15, 2026.
    - Review supporting documents by 10/10/2026.
    - URGENT: email client today to confirm missing records.
    """

    result = parse_workflow(text)

    assert result.contact.emails == ["jordan.lee@example.com"]
    assert result.contact.phone_numbers == ["(317) 555-0199"]
    assert date(2026, 10, 15) in result.dates_mentioned
    assert date(2026, 10, 10) in result.dates_mentioned
    assert len(result.action_items) == 2
    assert result.action_items[0].due_date == date(2026, 10, 10)
    assert result.action_items[1].priority == "high"


def test_ignores_invalid_dates() -> None:
    result = parse_workflow("Meeting 2026-02-31. Call client next week.")
    assert result.dates_mentioned == []
    assert len(result.action_items) == 1


def test_deduplicates_email_addresses() -> None:
    result = parse_workflow("Email a@b.com. Backup email a@b.com. Submit form.")
    assert result.contact.emails == ["a@b.com"]
