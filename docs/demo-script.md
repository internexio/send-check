# 3-minute demo script (THE SPEC: changes here change the build)

Live walkthrough of https://sendcheck.semalytics.com, two narrators, **3:00 hard cap**. The same script is the shot list for the judges' video. Words are timed at about 150 per minute; the live check takes 15 to 30 seconds, and the narration below is written to run over that wait, so nothing is dead air.

## Run of show

| Time | Who | On screen | Beat |
|---|---|---|---|
| 0:00 to 0:40 | Karen | Slide or the live page, no clicks | The problem and the Saltwind story |
| 0:40 to 2:10 | David | Live site: **Apology** example, Check draft, verdict, groups | The demo |
| 2:10 to 2:35 | David | Same screen, verdict still showing | Why this is different |
| 2:35 to 3:00 | Karen | Repo / plugin install line | Close |

## Narration

**[Karen, 0:00 to 0:40]** "Everyone in this room used AI to draft something this week, and most of it reads the same. At Hilton, my job was fixing AI copy so it was accurate, on brand, and made people want to travel. Small businesses have the same problem and nobody to fix it. A small business owner in the Washington AI survey told us: 'Preventing AI-slop is critical because it makes you look like an amateur.' Saltwind Kayak and Whale Tours. Their hired shuttle left 31 guests stranded at the ferry in August. Their AI-written apology is about to go to all 520 past guests."

**[David, 0:40 to 2:10, live]**

1. *(0:40, click **Apology**; the draft, five groups, and the 520-guest list all load)* "One click loads their draft and their guest list. I've saved my profile: Maren, co-owner, and the facts only she knows. The owners now drive the van, and a missed tour gets a refund or a free rebook."
2. *(0:55, click **Check draft**; the spinner shows)* "Send Check scores this draft against each group on the list, one at a time, using only facts from the list. It never invents a personality. Claude sees column summaries, never names or emails. This takes a few seconds, because a separate model is reading the draft as each group would."
3. *(1:15, verdict appears)* "Scrap. Every group needs changes. And notice what a style check says about this same draft: sounds human, one hundred. The writing is not the problem. The list is."
4. *(1:30, open the first group card)* "The 31 stranded guests paid for a tour that never ran. The draft offers them twenty percent off. They are owed a refund or a free rebook, and the draft never says their shuttle did not show."
5. *(1:45, open the 2027 group)* "The 58 guests with deposits on 2027 trips get an apology for problems they never had, months before their own pickup. They need to hear their booking is safe and who is driving the van. Here is the suggested version for that group. It ends with Maren's signature and cites only her facts. I approve it, copy it, and now it's mine."
6. *(2:00, scroll the remaining groups)* "Everyone who wasn't on those trips: don't send."

**[David, 2:10 to 2:35]** "Cursor ships an unslop skill. Anthropic's outreach skill runs a slop self-check. Both make the writer its own editor, and both pass this draft. Send Check is the independent editor. A separate model checks the draft against the people who will read it. It never sends anything."

**[Karen, 2:35 to 3:00]** "It installs as a Claude plugin in two commands, or runs as a web page, MIT-licensed. The owner approves every word. We checked this pitch with it: [READ THE SCORE AND VERDICT OFF THE SCREEN]. The repo is live."

## What is stable and what moves

The judge is a model, so numbers and some verdicts change from run to run. Narrate the stable parts and read everything else off the screen.

| Stable across our runs | Moves between runs |
|---|---|
| Overall verdict is **scrap** (45 to 47 in our Saltwind runs) | The exact overall score, by a few points |
| Every group needs changes (5 of 5) | Whether the **stranded** group shows fix or scrap, and the same for the **2027** group |
| Stranded: 20% off for a tour that never ran; they need a refund or free rebook | The exact words of each suggested version |
| 2027 bookers: apology and a discount for problems they never had | Group scores (44 to 67 seen) |
| Unaffected groups: an apology for something they were not part of | |
| Sounds human: 100 | |

So the script says what each group's problem is (stable) and never promises which group gets a suggested version. In step 5, if the 2027 group shows a version, use it. If not, open whichever group on screen does show one. If none does, say "for these groups the answer is don't send, and here is what each needs" and read the "what it needs" line.

## Before recording or presenting

1. Open https://sendcheck.semalytics.com in a clean window. It has no login. Use the dark or light theme, but keep one throughout.
2. Save **Your profile** in that browser: Maren Lindqvist, Co-owner, Saltwind Kayak & Whale Tours, saltwindtours.example, (360) 555-0142, hello@saltwindtours.example. "About your business" must include that the owners now drive the pickup van themselves, and that a guest whose tour was missed gets a full refund or a free rebooked trip. Without these, the stranded-guest refund finding and the van fact do not appear. Say "the owners' own policy", never imply Send Check inferred it.
3. Message type should read **To my customers** and the subject "An apology from all of us at Saltwind". Clicking **Apology** sets both.
4. **Pre-run the check once** right before going live. If it fails or is slow, you will know before the audience does.
5. Run the pitch text through Send Check and write down the real score and verdict for the close. Do not record with a placeholder.
6. Optional, if time allows: after **Apology** loads, press **Auto-segment** to show the groups being found from the guest list. Names, emails, and guest IDs are kept private and are listed as such on screen. Cut this first if running long.

## If something goes wrong on stage

- **Check is slow (over 40 seconds):** keep narrating step 2, then move to the contrast beat and return to the result when it lands.
- **Check errors:** reload, click **Apology**, run once more. If it fails twice, switch to the recorded video and say so.
- **Site is down:** run it locally with `uv run python -m web.app` at http://localhost:8000, same flow.
- **Over time:** cut step 6, then the Auto-segment option, then the 2027 beat's suggested version. Never cut the contrast beat or the close.

## Language rule

Describe Send Check with measurement verbs: scores, measures, flags, checks, diagnoses. The "suggested version" is a noun and is fine. Do not say it writes, generates, rewrites, or optimizes anything. No dashes in spoken or on-slide copy.

## Source material

- Example: fixture #21, `corpus/fixtures/21-tour-operator-apology-to-whole-guest-list.md`
- Guest list: `corpus/fixtures/data/saltwind-tours-guests.csv` (520 synthetic guests). The **Apology** button loads it automatically.
