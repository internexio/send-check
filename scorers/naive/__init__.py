"""Default backend. No external services required.

Three layers, cheapest first:
1. mechanical.py  - deterministic checks: length, you/I ratio, ask count,
                    reading level, personalization-token density
2. slop.py        - generic-phrase detection against corpus/generic_openers.txt
                    (n-gram overlap; no embeddings needed for v1)
3. judge.py       - Claude-as-judge with a structured rubric, scoring the
                    draft against the recipient context. Temperature 0,
                    JSON output conforming to DimensionScore.

combine.py merges the three into one Scorecard via verdict_from_score().
Build order at the event: mechanical -> slop -> judge. Each layer ships
independently; the pipeline works with whichever layers exist.
"""
