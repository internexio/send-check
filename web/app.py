"""Send Check web page: fill in the recipient and the draft, get a scorecard.

Run: uv run uvicorn web.app:app --reload   (or: uv run python -m web.app)
"""
from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Literal

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from scorers.base import Draft, Recipient
from scorers.env import load_env
from scorers.naive.combine import NaiveBackend
from scorers.segments import Segment, score_segments

PAGE = Path(__file__).resolve().parent / "static" / "index.html"

load_env()
app = FastAPI(title="Send Check")
backend = NaiveBackend()


class RecipientIn(BaseModel):
    name: str = ""
    role: str = ""
    company: str = ""
    context: str = ""


MessageType = Literal["cold", "follow_up", "warm", "post_meeting", "customer"]


class ScoreRequest(BaseModel):
    text: str
    subject: str = ""
    channel: Literal["email", "linkedin", "other"] = "email"
    message_type: MessageType = "cold"
    recipient: RecipientIn = RecipientIn()
    owner_samples: list[str] = []


class SegmentIn(BaseModel):
    label: str
    facts: str = ""
    size: int = 0


class ListRequest(BaseModel):
    text: str
    subject: str = ""
    channel: Literal["email", "linkedin", "other"] = "email"
    message_type: MessageType = "customer"
    segments: list[SegmentIn]
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


@app.post("/api/score_list")
def score_list(req: ListRequest) -> dict:
    result = score_segments(
        backend,
        Draft(text=req.text, channel=req.channel, subject=req.subject),
        [Segment(**s.model_dump()) for s in req.segments],
        message_type=req.message_type,
        owner_samples=[s for s in req.owner_samples if s.strip()],
        audience="segment",
    )
    return asdict(result)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
