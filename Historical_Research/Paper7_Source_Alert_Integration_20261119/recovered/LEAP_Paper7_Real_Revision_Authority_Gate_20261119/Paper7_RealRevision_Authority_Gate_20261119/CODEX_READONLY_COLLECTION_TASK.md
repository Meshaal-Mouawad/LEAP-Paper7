# CODEX TASK — Paper 7: read-only collection of authentic authority/deferral records

**Goal:** Locate original recorded business approvals/deferrals and link them to actual before/after KPI source revisions. This is an evidence extraction assignment, not an AI adjudication task. Do not edit, merge, commit, publish or change any repository, runtime ledger or database.

## Repository and baseline
- `Meshaal-Mouawad/AI-Powered_KPI_Extractor_Interactive_Bluebook_Generator`
- Current original research packet: `Paper7_RealRevision_Authority_Gate_20261119.zip` contains nine actual archived branch-source pairs and the blank reference instruments.
- In the archived main and branch Git objects, there are three unsigned override texts in historical `docs/overrides.json`, while the `kb/overrides.json`, `bluebook_generator/kb/overrides.json` and `docs/governance_overrides.json` ledgers contain no authenticated approval record in the inspected snapshots. PRs 5–7 were merged code changes without separate submitted review approvals. Do not count any of these as a signed business deferral.

## Collection workflow
1. Search **your current local Codex worktrees and authorized LEAP project data stores** for real approval and deferral audit evidence, including historical JSON/JSONL/CSV, SQLite databases (`-readonly`), approval workflow exports, screenshots/receipts, source review tickets, merge metadata, exception decisions and source-signature evidence. Search local untracked/ignored files if authorized; the supplied archive may not include them. Do not use private external systems without authorization.
2. For each authentic approval, export a **pseudonymized** row containing approval ID, status, role of human approver, date/time, exact KPI/finding, authorization scope, source hash/commit, applicable policy version, expiry/revocation, evidence path and checksum. Include adjacent source revisions and corresponding before/after finding outputs. Do not include usernames, emails, secrets, credentials or unredacted corporate data in the final package.
3. Report whether approved authorizations can be associated with source changes. If no record is found, produce a machine-readable `NO_AUTHENTIC_AUTHORIZATIONS_FOUND` result plus exact directories, revisions, tables and search expressions checked. Do not create synthetic approvals.
4. Provide an evidence-only packet for **two independent qualified human reviewers**. Record their signed/manual initial KEEP/REVOKE/UNKNOWN decisions *only after actual people supply them* and preserve evidence, disagreements and their resolution. Do not use AI to pretend to be a business approver or an independent human rater.
5. Keep the nine provided source transitions and the 24 constructed pilot cases in **separate strata**. Add more real source changes only when actual before/after snapshots are recoverable. Never turn a Git merge approval into a business authorization.

## Output contract
Return a ZIP (local only, do not publish) with `collection_manifest.csv`, `source_pairs/` (raw or redacted source), `authentic_approval_records.csv`, `source_findings_before_after.csv`, `evidence_hashes.csv`, `search_coverage.md`, and `adjudication_blind.csv`. For every data row cite the exact file/commit/DB table/query that supplies it. All absent data are blank or UNKNOWN, not invented. Include a reproducible read-only extraction script and a SHA-256 manifest. Ensure no personal identifiers or proprietary information is exported without approval.

**If records exist:** supply the evidence packet and original approval status, without assigning human KEEP/REVOKE labels yourself. **If records do not exist:** explicitly state so. A human authorization study cannot be completed from code history alone.
