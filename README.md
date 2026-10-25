<img src=".claude-plugin/icon.png" alt="Send Check logo" width="96">

# Send Check

**The missing skill: 44 skills in Claude for Small Business write for you. None of them score whether you should send it.**

Send Check is an open-source quality gate for AI-drafted email. Before a price increase, a win-back offer, an invoice reminder, or a cold email goes out, it scores the draft against the people who will actually read it and returns a verdict: **send, fix, or scrap**, with the evidence behind it and a fit-checked suggested fix you approve. It never sends anything.

> "Preventing AI-slop is critical because it makes you look like an amateur. I have not embraced full automation of many tasks because I don't trust or don't like the output."
> — small business owner, WA Small Business AI Survey, Oct 2026

## One email to many people is many emails

A small business rarely writes to one person. It sends one draft to a whole list, and the people on that list are in very different situations. Send Check splits the list into segments by facts the business already has (how long they've been customers, last visit, rate, payment history) and checks the draft from each group's side.

Example: Cascade Self Storage raises rates 12% for 340 renters with one "our costs went up" email. Send Check measures it per segment:

| Segment | People | Verdict | The fact behind it |
|---|---|---|---|
| Negotiated rate | 90 | **Scrap / hold** | Rate agreement on file: a blanket 12% reads as overriding it. Don't send until each agreement is checked |
| Moved in under 6 months | 140 | Fix | A 12% rise weeks after signing at a quoted price reads as bait-and-switch |
| Tenants 5+ years | 66 | Fix | Median tenure 13.8 years, and they get the same form letter as last month's move-ins |
| Commercial, invoiced | 32 | Fix | Nothing about which invoice the new amount starts on |

Each failing segment comes with its own version of the email to approve. (Verdicts vary a little from run to run; the facts behind them are stable.)

## Try it

### The web page

```bash
git clone https://github.com/internexio/send-check && cd send-check
uv sync
cp .env.example .env        # then add ANTHROPIC_API_KEY
uv run python -m web.app    # open http://localhost:8000
```

1. **Your email:** paste the draft, or click an example (Price increase, Win-back, Cold email).
2. **Who it's for:**
   - **One person:** name, role, company, an optional company website, and what you know about them.
   - **A list:** upload a customer list (CSV or Excel), drop it on the box, or paste it, then press **Auto-segment**. Or add segments by hand. A synthetic 340-customer sample list is built in.
3. **Check draft.** You get the verdict per segment, the evidence, and a suggested version for each group that needs one.

Save **Your profile** once (name, company, signature, what your business offers, a few emails you've sent). It stays in your browser, and every check uses it: suggested fixes end with your exact signature and cite only the facts you gave, and "sounds like you" uses your saved emails.

Without an API key, the page still scores generic phrasing, style, and length, and estimates the rest.

### The Claude plugin

In Claude Code:

```bash
claude plugin marketplace add internexio/send-check
claude plugin install send-check@send-check
```

Then use Claude as usual:

- **It runs on its own.** Ask Claude to write a customer email or outreach, and Send Check scores the draft before Claude shows it to you.
- **Check a draft:** "Should I send this to Dana? Here's the email … and her bio …"
- **Check against your customer list:** "Check this price-increase email against customers.csv." Send Check profiles the file locally, proposes segments, and returns a verdict per segment.

The first time it runs, Claude Code asks you to allow the Send Check skill. That one approval lets it run its own check scripts for that turn. The plugin needs nothing else installed: its scripts use the Python standard library.

## How it scores

Three layers, cheapest first, merged into one scorecard:

1. **Deterministic checks** (`scorers/naive/mechanical.py`, `slop.py`, `voice.py`): generic phrases from Anthropic's and Cursor's own slop lists (`corpus/ATTRIBUTION.md`), length for the message type, the ask, AI style tells (uniform sentences and paragraphs, missing contractions), and an optional match against emails the owner actually sent.
2. **A Claude judge** (`scorers/naive/judge.py`): scores personalization and fit for this recipient or segment, names the fact behind every finding, and proposes a fit-checked suggested fix. It runs on its own model (`SENDCHECK_JUDGE_MODEL`, default `claude-opus-5-5`), separate from whatever drafted the email.
3. **One shared rubric** (`skills/send-check/reference/rubric.md`), used by both the page and the plugin. It includes:
   - **Facts, not personas.** Segments are judged only on observable facts, never invented personalities.
   - **Disqualifying tells** from the team's [humanization rubric](docs/humanization-rubric.md) cap a draft at scrap: an unfilled merge field, leftover assistant text ("Certainly! Here's a draft"), a fake "Re:", flattery as the only personalization.
   - **Stakes-based pass lines.** Cold outreach needs 82+ to send; client mail needs 75.
   - **Always-flag misses.** "Our costs went up" as the reason for a price increase does no better than giving no reason (2026 field experiment).
   - **"Don't send to this group"** is a valid fix.

For a list, every segment is scored in parallel. The worst segment decides the verdict, and scores are weighted by segment size.

## Privacy

- **Customer lists stay local.** Claude sees only column summaries (ranges, common values, counts). Names, emails, phone numbers, addresses, IDs, free-text columns, and protected characteristics are dropped before anything is summarized. Python applies the proposed segment rules to the real rows. The plugin's `segment_csv.py` works the same way, and the skill tells Claude never to open the file itself.
- **No social media.** The company-website box reads a public business page only. It refuses LinkedIn, X, Instagram, and other social profiles, and any non-public address.
- **Nothing is sent.** Send Check measures; the owner approves every word.

## Does it work?

All 20 synthetic small-business scenarios in `corpus/fixtures/` were scored per segment and graded against the problems each one is expected to raise:

**56 of 71 expected problems caught (79%). 6 of 7 clean cases passed without a false alarm.**

Full results: [`corpus/validation/eval-results.md`](corpus/validation/eval-results.md). To rerun it (about 2.5 minutes and roughly 80 API calls):

```bash
uv run python scripts/eval_fixtures.py          # or pick fixtures: ... 1 9 12 16
uv run pytest -q                                # unit tests, no API calls
```

## Why this exists when slop checkers exist

Cursor ships unslop, a rewrite skill. Anthropic's outreach-composer runs a slop self-test, a checklist the writer applies to itself. Lavender scores email structure. Each makes the writer its own editor, or checks style without the reader.

Send Check is the independent instrument: any draft from any source, measured against the actual recipients, returning a verdict you can gate on.

## Scoring backends (pluggable)

| Backend | What it measures | Status |
|---|---|---|
| `naive` (default) | The three layers above | Built. Needs only `ANTHROPIC_API_KEY` |
| `semalytics` | Audience fit against peer-reviewed personality and persuasion frameworks, reproducibly ([what it adds](docs/semalytics-backend-api.md)) | Adapter in progress. Needs `SENDCHECK_SEMALYTICS_KEY` |

Every backend implements `ScoringBackend` in `scorers/base.py`, and `scorers/segments.py` scores lists with any of them.

## Repository map

| Path | What's there |
|---|---|
| `web/` | FastAPI app and the single-page UI |
| `scorers/` | Scoring contract (`base.py`), naive backend, segments, auto-segmentation, website reader |
| `skills/send-check/` | The plugin skill: `SKILL.md`, the shared rubric, and the stdlib check scripts |
| `.claude-plugin/` | Plugin and marketplace manifests |
| `corpus/` | Phrase lists with attribution, 20 synthetic test emails, sample customer list, eval results |
| `docs/` | Use cases, humanization rubric, test recipients, SEMalytics notes, plan and demo script |
| `scripts/` | Fixture eval and sample-data generator |

## Status

Built at the Claude Seattle Impact Lab hackathon, Oct 2026. Scaffold (interfaces, docs, CI) prepared the night before kickoff; implementations built at the event.

Roadmap: the SEMalytics adapter, a score log for score-to-reply analysis, and checks inside Gmail and CRMs.

**IP note:** the SEMalytics scoring API is pre-existing technology and is out of scope of hackathon-built work. This repository contains no SEMalytics internals, only a thin adapter to its public endpoint.

## License

MIT
