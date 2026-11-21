# Paper 7 — Independent authorization reference instrument

## Record identity and evidence

Each row is one **actual authorization evaluated across one source revision**. Record an authentic signed approval/deferral or review-action identifier, its scope, finding identity, source revision, affected policy, owner, status, expiry, and direct document or audit-log evidence. A code change alone is not an approval decision.

## Outcome rules

A reference outcome of `KEEP` requires a valid active approval, matched finding identity, valid approval scope, applicable policy, and documented evidence that the subsequent source state remains within its authorized scope. `REVOKE` requires a documented invalidation condition: relevant changed evidence, expired approval, revoked approval, different authority/policy, or explicit rejection. `UNKNOWN` is mandatory when authenticity, scope, change relevance, or status cannot be established from the available record.

Approve/revoke is a **business/reviewer authority decision**. A source hash, unchanged Boolean warning, or a static analyzer result alone is not the human reference. Collect the source diff and both finding records. Perform the reference adjudication **before** running candidate strategies on the held-out set.

## Adjudication

Two eligible domain reviewers should independently judge each record from masked evidence without seeing the candidate strategies' predictions. Retain initial labels, disagreements, rationale, resolution and dates; define the adjudication rule in advance. Do not simulate reviewers, certify AI-generated labels as human approval, or treat reviewer self-reports as captured field observations.

## Study design

Use unrelated source-change groups or repositories for final held-out evaluation. Separate authentic approval records from controlled mutations. Count approval decisions as the primary unit; cluster dependent repeated events under their parent approval/source revision. Report false-retained, false-revoked, and `UNKNOWN` separately. Match the same event/deferral/expiry/policy conditions across all strategies.

## Current collection state

No rows have been added because the inspected original `kb/overrides.json`, `bluebook_generator/kb/overrides.json`, and `docs/governance_overrides.json` ledgers have zero approval entries. This template is a prospective instrument, not a dataset with simulated results.
