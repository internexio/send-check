"""combine.py: the naive backend end to end, judge off (no API calls)."""
import pytest

from scorers.base import Draft, Recipient
from scorers.naive.combine import NaiveBackend


@pytest.fixture(autouse=True)
def judge_off(monkeypatch):
    monkeypatch.setenv("SENDCHECK_JUDGE", "off")


def test_sloppy_draft_cannot_send():
    card = NaiveBackend().score(
        Draft(text="Hi Dana,\nI hope this email finds you well. We help companies like yours "
                   "unlock growth. Would you be open to a quick call?"),
        Recipient(name="Dana", company="Northside", context="Posted about Fremont scheduling mix-ups"),
    )
    assert card.verdict in ("fix", "scrap")
    assert card.score <= 74
    assert "blocks send" in card.notes
    assert [d.name for d in card.dimensions] == ["slop", "personalization", "recipient_fit", "mechanics"]


def test_voice_samples_add_evidence():
    card = NaiveBackend().score(
        Draft(text="Dear Pat,\nI am writing about your new unit. Do you want a quote?\n\nBest regards,\nDana"),
        Recipient(),
        owner_samples=["Hey Sam,\nWe can't make Tuesday but I'll bring samples. Works?\n\nCheers,\nDana"],
    )
    slop = card.dimensions[0]
    assert any("you open with" in e for e in slop.evidence)


def test_never_raises_on_bad_input():
    card = NaiveBackend().score(Draft(text=None), Recipient())
    assert card.verdict == "fix"
    assert card.notes.startswith("scoring failed")


def test_disqualifying_tell_caps_at_scrap():
    card = NaiveBackend().score(
        Draft(text="Certainly! Here's a draft:\n\nHi Dana, saw your Fremont post. Want a demo Friday?"),
        Recipient(name="Dana", context="Posted about the Fremont remodel"),
    )
    assert card.score <= 30 and card.verdict == "scrap"
    assert "disqualified: P20a" in card.notes


def test_template_tell_allowance_is_stricter_for_cold():
    text = ("Hi Dana,\nI wanted to reach out about the Fremont job. "
            "Let me know if this resonates. Looking forward to connecting. Want a demo Friday?")
    cold = NaiveBackend().score(Draft(text=text), Recipient(), message_type="cold")
    assert "template tells; a cold message allows 1" in cold.notes
    assert cold.score <= 74


def test_list_template_merge_fields_are_a_reminder_not_a_cap():
    card = NaiveBackend().score(Draft(text="Hi [First Name],\nYour rate becomes [New Rate] on December 1."),
                                Recipient(name="10-year tenants"), message_type="customer",
                                audience="segment")
    assert "disqualified" not in card.notes
    assert "fill the merge fields before sending" in card.notes
