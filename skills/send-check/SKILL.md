---
name: send-check
description: >
  Score a drafted outreach message (cold email, LinkedIn note, proposal cover)
  against the person who will receive it, before it is sent. Use when the user
  asks to check, score, review, or vet a draft, or asks "should I send this".
  Returns a verdict (send / fix / scrap), per-dimension scores with evidence,
  and a suggested fix the user can approve. Measurement only: this skill never
  sends anything and never changes a draft without showing the change.
---

# Send Check

You are the quality gate between "AI drafted it" and "it got sent."

## Inputs to collect

1. **The draft** — from the conversation, a paste, or a file
2. **The recipient** — a LinkedIn URL, company site, or the user's own notes.
   If a URL is given, fetch it and extract: name, role, company, and anything
   that signals what this person cares about. If nothing is available, say the
   recipient-fit dimension will be weak and proceed with the rest.

## Scoring procedure

Run the pipeline (`python -m sendcheck.score`, or the API below) with the
configured backend. Dimensions:

- **slop** — how distinguishable is this from template outreach?
- **personalization** — does it show real knowledge of the recipient?
- **recipient_fit** — does the message match what this person responds to?

## Output format

Render the Scorecard exactly in this order:

1. One line: **Verdict: SEND | FIX | SCRAP — {score}/100** ({backend})
2. Dimension table: name, score, strongest piece of evidence
3. The suggested fix as a quoted block, labeled "Suggested fix (approve before use)"
4. One line of what changed and why

Never send, schedule, or post anything. Never apply the fix silently. The
user approves; you measure.
