"""Send Check web page: fill in the recipient and the draft, get a scorecard.

Run: uv run uvicorn web.app:app --reload   (or: uv run python -m web.app)
"""
from __future__ import annotations

import base64
from dataclasses import asdict
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel

from scorers.autosegment import autosegment, xlsx_to_csv
from scorers.base import Draft, Recipient
from scorers.env import load_env
from scorers.naive.combine import NaiveBackend
from scorers.segments import Segment, score_segments

PAGE = Path(__file__).resolve().parent / "static" / "index.html"
SAMPLE_CSV = (Path(__file__).resolve().parents[1]
              / "corpus" / "fixtures" / "data" / "cascade-storage-customers.csv")

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


class CsvRequest(BaseModel):
    csv_text: str = ""
    xlsx_base64: str = ""      # an Excel file, read on the server
    text: str
    subject: str = ""


@app.get("/", response_class=HTMLResponse)
def page() -> str:
    return PAGE.read_text(encoding="utf-8")


@app.get("/api/sample_csv", response_class=PlainTextResponse)
def sample_csv() -> str:
    return SAMPLE_CSV.read_text(encoding="utf-8")


@app.post("/api/segment_csv")
def segment_csv(req: CsvRequest) -> dict:
    if not req.text.strip():
        raise HTTPException(400, "paste the draft first: segments depend on what you are sending")
    try:
        csv_text = req.csv_text
        if req.xlsx_base64:
            try:
                csv_text = xlsx_to_csv(base64.b64decode(req.xlsx_base64))
            except Exception:
                raise ValueError("couldn't read that Excel file; try saving it as CSV")
        if not csv_text.strip():
            raise ValueError("the file is empty")
        return asdict(autosegment(csv_text, req.text, req.subject))
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(502, f"could not propose segments: {e}")


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
