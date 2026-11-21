# Paper 7 — Real historical KPI source-revision authority gate (2026-11-19)

**Scientific state:** real-source evidence prepared; no genuine human business-approval reference recovered; manuscript held.

## Key files

- `reports/Scientific_Gate_Update_20261119.pdf` — scientific assessment and gate result.
- `data/real_source_revisions.csv` — 9 actual archive-backed source pairs, exact hashes, history identities, technical comparison classes.
- `cases/P7R01` … `cases/P7R09` — full original before/after source bytes, unified diffs, provenance notes.
- `scripts/verify_source_pairs.py` — verify source bytes/hashes and technical comparison outcomes **without** Git.
- `scripts/verify_python_source_behavior.py` — verify two AST-equal cases and one standalone Python behavior change.
- `data/github_merges_not_approvals.csv` — three code-merge PRs distinguished from a business authorization.
- `data/authenticated_authorizations_blank.csv` — empty source of actual authorization fields; not fake approval entries.
- `data/reviewer_adjudication_blind.csv` — two blank human-review slots per source pair.
- `scripts/check_authorization_gate.py` — refuses to score approvals absent authenticated records and real dual judgments.
- `protocol/Prospective_Authorization_Adjudication.md` — independent human-reference procedure.
- `CODEX_READONLY_COLLECTION_TASK.md` — exact read-only Codex extraction task.

## Checks

```bash
python scripts/verify_source_pairs.py
python scripts/verify_python_source_behavior.py
python scripts/check_authorization_gate.py  # expected exit 2 = BLOCKED
```

The original LEAP `.git` archive was not copied into this package (approximately 169 MB ZIP). The nine complete source-file snapshots and SHA-256 hashes permit independent verification of the comparisons without that archive. The unchanged earlier controlled pilot ZIP is included in `inputs/`, and its fresh replay log is in `reports/`. `data/all_ref_source_events.csv` contains the full scan inventory (223 code status events). Full commit-history re-extraction requires the original user-provided LEAP repository ZIP, whose data was read without modifying it.

**Provenance:** original project files supplied by the user, private connected GitHub metadata from the user's repository, prior frozen Paper 7 pilot. No private source was published to an external repository.
