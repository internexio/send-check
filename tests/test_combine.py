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
