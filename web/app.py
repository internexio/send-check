"""Send Check web page: fill in the recipient and the draft, get a scorecard.

Run: uv run uvicorn web.app:app --reload   (or: uv run python -m web.app)
"""
from __future__ import annotations

import os
from dataclasses import asdict
from pathlib import Path
from typing import Literal

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from scorers.base import Draft, Recipient
from scorers.naive.combine import NaiveBackend

ROOT = Path(__file__).resolve().parents[1]
PAGE = Path(__file__).resolve().parent / "static" / "index.html"


def _load_env(path: Path = ROOT / ".env") -> None:
    """Read KEY=value lines from .env without overriding the real environment."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        key, sep, value = line.partition("=")
        value = value.split("#", 1)[0].strip()
        if sep and key.strip() and not key.startswith("#") and value:
            os.environ.setdefault(key.strip(), value)


_load_env()
app = FastAPI(title="Send Check")
backend = NaiveBackend()


class RecipientIn(BaseModel):
    name: str = ""
    role: str = ""
    company: str = ""
    context: str = ""


class ScoreRequest(BaseModel):
    text: str
    subject: str = ""
    channel: Literal["email", "linkedin", "other"] = "email"
    message_type: Literal["cold", "follow_up", "warm", "post_meeting"] = "cold"
    recipient: RecipientIn = RecipientIn()
    owner_samples: list[str] = []


@app.get("/", response_class=HTMLResponse)
def page() -> str:
    return PAGE.read_text(encoding="utf-8")


@app.post("/api/score")
def score(req: ScoreRequest) -> dict:
    card = backend.score(
        Draft(text=req.text, channel=req.channel, subject=req.subject),
        Recipient(**req.recipient.model_dump()),
        message_type=req.message_type,
        owner_samples=[s for s in req.owner_samples if s.strip()],
    )
    return asdict(card)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
