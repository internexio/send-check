# 90-second demo script (THE SPEC — changes here change the build)

Final script. Screen recording of the paste → list → verdict per segment → fix flow, two narrators. Record at H6. Re-record only if time allows.

**NOTE: every score below must be a REAL score from the take you record. Today's run gave SCRAP 45, stranded guests FIX 56, sounds human 88; verdicts are stable but numbers move a few points between runs, so read them off the screen before recording the voiceover. The "81, send" in the last beat comes from running the actual pitch text through Send Check at H6. Do not record with a placeholder number.**

**[Karen, 20s]** "Everyone in this room has used AI to draft content, and most of it reads the same. Every day in my role at Hilton, I revamped AI-generated copy so that the messaging inspired people to explore new destinations and hidden treasures, beyond being accurate and on-brand. Small businesses struggle with the same marketing issues, but have fewer people available to help. Here's one example from a two-person, mom-and-pop kayak tour company. Their shuttle stranded 31 guests at the ferry in August. Their AI-written apology went to all 520 past guests."

**[David, 35s, live]** "Paste the draft, upload the guest list. Send Check splits it by facts the owners already have, and the names never leave the machine. Verdict: scrap. Only the 31 stranded guests get a fix: the draft never says their shuttle didn't show, and 20% off isn't a make-good when the owners' own policy promises a refund or a free rebook. The other 489, including 58 with deposits on 2027 trips, get scrap: don't send. Here's the suggested fix for the 31. I approve it, now it's mine." *(paste → upload → auto-segment → verdict per group → fix on screen)*

**[David, 20s, contrast]** "Cursor ships an unslop skill. Anthropic's own outreach skill runs a slop self-check. Both make the writer its own editor, and a style check passes this draft: Send Check scores it 88, sounds human. The writing isn't the problem. The list is. Send Check is the independent editor that checks the draft against the people who will read it."

**[Karen, 15s]** "MIT-licensed, installs as a Claude skill in the official plugin style. We scored this pitch with it: 81, send. Repo's live."

## Recording setup

- Example: fixture #21, `corpus/fixtures/21-tour-operator-apology-to-whole-guest-list.md`. Guest list: `corpus/fixtures/data/saltwind-tours-guests.csv` (520 synthetic guests).
- Before recording, save **Your profile** in the browser you record from: Maren Lindqvist, Co-owner, Saltwind Kayak & Whale Tours, saltwindtours.example, (360) 555-0142, hello@saltwindtours.example. "About your business" must include that the owners now drive the pickup van themselves and the refund-or-rebook policy; without them the stranded-guest refund finding and the van fact do not appear.
- Message type: **To customers**. Subject: "An apology from all of us at Saltwind".
- After Auto-segment, delete any leftover "Everyone else" group with its × so the screen shows four groups: stranded 31, 2027 deposits 58, toured this summer, lapsed.
- The 31-guest refund finding comes from the policy in the profile. Say "the owners' own policy", never imply Send Check inferred it.
