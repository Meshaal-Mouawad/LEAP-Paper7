# Post-evaluation verification amendment — 18 November 2026

The frozen v1 protocol, code and references remain unchanged. The final independent AI reviewer found that oracle v1 defaulted an absent required event unit to seconds. The tested monitor correctly rejected this malformed input. No evaluated valid trace omitted unit.

A separate `implementation/oracle_v2.py` removes the default. Independent `reviews/check_oracle_v2.py` verifies 28 malformed-schema cases for both corrected oracle and monitor, and equality with all 4,935 frozen benchmark and 60 witness output sequences. This is a schema correction with unchanged reported valid-input results. Frozen v1 is retained for exact reproduction; new independent checking should use v2.

The reviewer also ran an exploratory 2,000-case seeded variable-policy differential audit. It is post-evaluation verification, not an expansion of the frozen sample or a new confirmatory performance result. Main denominators are unchanged.

The generic information-class counting audit was added after primary scoring to recompute the already-frozen pair witnesses. No new witness input or reference was added. Witness severity is fixed to High as encoded in freeze.py; performance benchmark severity uses recovered categorical labels. The manuscript now states that distinction.
