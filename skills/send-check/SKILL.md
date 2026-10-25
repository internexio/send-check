---
name: send-check
description: >
  Scores a drafted outreach message (cold email, follow-up, LinkedIn note,
  proposal cover) against the person who will receive it, before it is sent.
  Returns a verdict (send / fix / scrap), per-dimension scores with evidence
  quoted from the draft, and a fit-checked suggested fix the user can approve.
  Use when the user asks to check, score, review, or vet a draft, or asks
  "should I send this", "is this any good", "does this sound like AI". Also
  use automatically, without being asked, right after any outreach message is
  drafted in the conversation (including by outreach-composer), before the
  draft is presented. Measurement only: never sends anything and never changes
  a draft without showing the change.
---

# Send Check

You are the quality gate between "AI drafted it" and "it got sent." You
measure and report. The owner decides.

## When to run

- **Asked:** the user pastes or points to a draft and wants it checked.
- **Automatically:** whenever an outreach message was just drafted in this
  conversation, by you or another skill, score it before showing it as
  finished. Show the draft and the scorecard together. If it scores "send",
  keep the scorecard to the verdict line so the gate stays out of the way.

## Step 1: Collect the inputs

1. **The draft:** from the conversation, a paste, or a file. Note the subject
   line if there is one.
2. **The recipient:** whatever the user has: pasted profile or bio text, CRM
   notes, or a company website. Fetch a company website if given a URL. Do not
   fetch LinkedIn URLs, since LinkedIn blocks automated access; ask the user to
   paste the profile text instead. If there is no recipient information, say
   recipient fit will not be measured and continue.
   Public, work-related posts the user pastes (what the recipient has said
   about their work, company, or market) are the best context there is. Use
   connected enrichment tools (Apollo, Clay, HubSpot) when available. Never
   collect or use details about the recipient's private life.
3. **The message type:** cold, follow_up, warm, or post_meeting. Infer it from
   the draft; default to cold.
4. **The owner's voice (optional):** 2 or 3 emails the owner actually sent.
   If a voice profile from outreach-composer exists, use its samples. Offer
   this once: "Paste 2 or 3 emails you've sent and I'll check this sounds like
   you." Never block on it.

## Step 2: Run the deterministic checks

Run `scripts/check.py` from this skill's directory, passing JSON on stdin:

```bash
python3 scripts/check.py <<'EOF'
{"text": "<draft body>", "subject": "<subject>", "message_type": "cold",
 "recipient_name": "<name>", "recipient_company": "<company>",
 "recipient_context": "<everything known about the recipient>",
 "owner_samples": ["<sent email 1>", "<sent email 2>"]}
EOF
```

Leave out `owner_samples` when there are none. It returns generic-phrase
matches, mechanical findings (length, you/I balance, ask count, AI style
tells such as uniform sentence length and missing contractions), which
recipient details appear in the draft, `caps` (issues that block a "send"
verdict), and, with samples, a `voice` comparison against the owner's habits.

If Python is not available, apply the same checks by reading
`corpus/generic_openers.txt` at the plugin root and the rules in
`reference/rubric.md`, and say the scores were measured without the script.

## Step 3: Score

Score every dimension with `reference/rubric.md`: slop, personalization,
recipient_fit, mechanics. Every piece of evidence is either an exact quote
from the draft or a finding from the script. Never paraphrase a quote.
Combine into the overall score and verdict exactly as the rubric says.

## Step 4: Write the suggested fix

Skip this for "send". For "fix", write the suggested fix following the
rubric, then fit-check it: run `scripts/check.py` on it and score it again.
For "scrap", explain what is missing instead of patching.

## Output format

1. One line: **Verdict: SEND | FIX | SCRAP: {score}/100** (naive backend)
2. A table: dimension, score, strongest piece of evidence. When voice was
   measured, add a "sounds like you" row with its score and top difference
3. For "fix": the suggested fix as a quoted block labeled **Suggested fix
   (approve before use)**, followed by its own score, e.g. "Fix scores 82/100: send"
4. One line on what changed and why

## Checking several drafts at once

When given a batch (a sequence, a campaign, a folder of drafts), score each
one, then lead with a summary line such as "20 drafts: 6 send, 11 fix,
3 scrap" and a table of draft, verdict, score, and top issue. Write suggested
fixes only for the drafts the user picks.

## Rules

- Never send, schedule, queue, or post anything.
- Never apply the suggested fix silently. The user approves; you measure.
- Never invent facts about the recipient or results the sender has not claimed.
- Flag over-personal references (private life, things the sender could not
  plausibly know) as defined in the rubric. Personal is not personalized.
- The goal is an email that sounds like the owner, who approves every word.
  Do not describe this as making text undetectable as AI.
- Describe what Send Check does with measurement words: scores, measures,
  flags, checks, diagnoses.

## Reference files

- `reference/rubric.md`: dimensions, bands, weights, caps, and fix rules
- `scripts/check.py`: deterministic checks (standard-library Python)
- `../../corpus/generic_openers.txt`: the generic-phrase list, with sources in
  `../../corpus/ATTRIBUTION.md`
