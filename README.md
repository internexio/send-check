# Send Check

**The missing skill: 44 skills in Claude for Small Business write for you. None of them score whether you should send it.**

Send Check is an open-source quality gate for AI-drafted outreach. Before a cold email, proposal, or post ships, Send Check scores the draft against the actual recipient and returns a verdict: **send, fix, or scrap** — with the evidence and a fit-checked fix.

> "Preventing AI-slop is critical because it makes you look like an amateur. I have not embraced full automation of many tasks because I don't trust or don't like the output."
> — small business owner, WA Small Business AI Survey, Oct 2026

## What it does

1. Takes a draft + recipient context (a LinkedIn URL, a website, CRM notes)
2. Scores it on slop detection, personalization depth, and recipient fit
3. Returns a scorecard: verdict, per-dimension evidence, and a suggested fix
4. Logs what was scored, for score-to-reply analysis (roadmap)

## Use it two ways

- **As a Claude skill** — `/send-check` inside Claude, in the style of the official [Claude for Small Business plugin](https://github.com/anthropics/knowledge-work-plugins)
- **As a web page** — paste a draft, get a verdict in seconds

## Scoring backends (pluggable)

| Backend | What it measures | Requires |
|---|---|---|
| `naive` (default, built-in) | Generic-phrase detection, mechanical checks, structured Claude-as-judge rubric | Nothing. Works out of the box |
| `semalytics` | Audience-fit measurement against peer-reviewed personality research | `SENDCHECK_SEMALYTICS_KEY` |

The default backend asks "is this good outreach?" The SEMalytics backend measures "does this fit *this person*, reproducibly, against validated frameworks" — and catches mismatches a generic judge can't see.

## Quickstart

```bash
git clone https://github.com/SEMalytics/send-check && cd send-check
uv sync
cp .env.example .env   # optional: add keys
uv run python -m web.app   # paste-box demo at localhost:8000
```

## Status

Built at the Claude Seattle Impact Lab hackathon, Oct 2026. Scaffold (interfaces, docs, CI) prepared the night before kickoff; implementations built at the event.

**IP note:** the SEMalytics scoring API is pre-existing technology and is out of scope of hackathon-built work. This repository contains no SEMalytics internals — only a thin adapter to its public endpoint.

## License

MIT
