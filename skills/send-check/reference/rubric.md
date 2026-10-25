# Send Check scoring rubric

The single source of scoring rules. The skill reads this file; the web
backend's judge loads the same file, so both measure the same way.

Every score is an integer from 0 to 100. Score against the bands below, not
against a feeling. The same draft and recipient should get the same score
every time, so when a draft sits between two bands, pick the lower one.

## Dimensions

### slop (weight 25): how distinguishable is this from template outreach?

Take `slop.score` from `scripts/check.py` as the score. Then deduct the
points of any mechanical findings named `em_dash`, `uniform_paragraphs`, or
`three_bullets`, since those are style tells too.

Evidence: quote each matched phrase exactly as it appears in the draft,
strongest first. If the script could not run, find the phrases by reading
`corpus/generic_openers.txt` (at the plugin root) and apply the same weights:
15 points per phrase of 3+ words, 8 per 2-word phrase, 4 per single word.

### personalization (weight 30): does it show real knowledge of the recipient?

| Band | What it looks like |
|---|---|
| 90–100 | Could only have been sent to this person. Uses a specific, checkable detail from the recipient context and ties it to why the sender is writing |
| 60–89 | Uses a real detail, but the link to the reason for writing is loose |
| 30–59 | Only merge fields (name, company, title) or vague category fit ("businesses like yours") |
| 0–29 | Nothing specific, or a fake-warm opener: flattery, "I've been following your work", an invented connection |

If `recipient_terms_found` is empty and recipient context was given, the
score is at most 40. Evidence: quote the line that carries the detail, or the
line where a detail should have been.

### recipient_fit (weight 30): does the message match what this person responds to?

Judge the offer, the tone, and the ask against the recipient's role,
seniority, and stated priorities.

| Band | What it looks like |
|---|---|
| 90–100 | The offer maps to a priority visible in the context; tone matches their seniority and style; the ask is sized for them |
| 60–89 | Relevant offer, but tone or ask is off (too formal, too casual, too big an ask for a first touch) |
| 30–59 | A generic offer that would fit anyone in the category |
| 0–29 | Mismatched: wrong role, irrelevant offer, or a tone this person would find off-putting |

With no recipient information at all, score 50 and say in the evidence that
recipient fit was not measured.

### mechanics (weight 15): length, balance, and the ask

Start at 100 and deduct the points of every mechanical finding except
`personalization`, `em_dash`, `uniform_paragraphs`, and `three_bullets`
(those are counted above). Evidence: each finding's `detail`.

## Overall score and verdict

```
overall = round(0.25 * slop + 0.30 * personalization + 0.30 * recipient_fit + 0.15 * mechanics)
```

If `caps` from the script is not empty, overall is at most 74: a capped
draft cannot get "send" until the capped issue is fixed.

Verdict, matching `verdict_from_score()` in `scorers/base.py`:

| Overall | Verdict |
|---|---|
| 75–100 | send |
| 45–74 | fix |
| 0–44 | scrap |

## The suggested fix

- Keep the owner's voice, facts, and offer. Change only what the evidence flagged.
- Never invent facts: no made-up results, customers, mutual connections, or
  details about the recipient. When a fix needs a detail only the owner knows,
  leave a bracketed placeholder such as `[the project of theirs you liked]`.
- Stay under the length ceiling, with exactly one small ask.
- Fit-check it: run `scripts/check.py` on the fix and score it with this same
  rubric. A suggested fix must reach "send" with no caps. If it cannot without
  a fact the owner has to supply, say so instead of padding it.
- For a "scrap" verdict, do not patch the draft. Say what it would need (a
  real reason to write to this person) and offer to help find one.
