"""Deterministic Send Check signals for one draft, as JSON.

Usage: pipe a JSON object on stdin, get JSON on stdout.

    {"text": "...", "subject": "...", "message_type": "cold",
     "recipient_name": "Dana Lee", "recipient_company": "Northside Remodeling",
     "recipient_context": "bio, CRM notes, site copy",
     "owner_samples": ["an email the owner actually sent", "..."]}

message_type is one of cold, follow_up, warm, post_meeting (default cold).
owner_samples is optional; with it, the output includes a voice match.
Standard library only. Runs from the plugin root layout:
skills/send-check/scripts/check.py -> scorers/naive/.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))


def main() -> None:
    try:
        from scorers.naive import mechanical, slop, voice
    except ImportError as e:
        print(json.dumps({"error": f"scorers not found next to the skill: {e}"}))
        return

    try:
        req = json.load(sys.stdin)
        text = req["text"]
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(json.dumps({"error": f"expected JSON with a 'text' field: {e}"}))
        return

    mech = mechanical.check(
        text,
        message_type=req.get("message_type", "cold"),
        recipient_context=req.get("recipient_context", ""),
        recipient_name=req.get("recipient_name", ""),
        recipient_company=req.get("recipient_company", ""),
    )
    try:
        sl = slop.check(text)
    except OSError as e:
        sl = {"score": None, "matches": [], "generic_opener": False,
              "error": f"phrase list unavailable: {e}"}

    caps = [f["detail"] for f in mech["findings"] if f["cap"]]
    if sl["generic_opener"]:
        opener = next(m["phrase"] for m in sl["matches"] if m["in_opener"] and m["words"] >= 3)
        caps.append(f'opens with a generic phrase: "{opener}"')

    out = {"mechanical": mech, "slop": sl, "caps": caps}
    samples = req.get("owner_samples") or []
    if samples:
        out["voice"] = voice.compare(text, samples)
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
