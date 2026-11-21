# Paper 7: prospective independent authorization-reference protocol

## Scientific question
For an authentic business-approved governance deferral associated with a source-derived finding, does a subsequent source change preserve the authorization's evidential scope, or invalidate it? The outcome is `KEEP`, `REVOKE`, or `UNKNOWN`. A Git commit or source-code-equivalence result is evidence about the source, not a business authorization.

## Study cohort and source provenance
The nine packets in `cases/P7R01`-`P7R09` are **actual archived non-main-branch source revisions**, not user approvals. They are candidate source-change exemplars. Select only those with authentic linked approval records for primary field evaluation. Prospective cases from additional repositories may be added if the original source and approved deferral records exist; maintain provenance and site linkage. Frozen Paper 7 and 24-case controlled pilot data are comparison diagnostics, not validation labels.

## Authenticity gate
A record is eligible for `KEEP`/`REVOKE` only when its original approval ID, approved/pending/rejected status, approver role, timestamp, scope, source/finding identity, policy version and expiry can be linked to a primary immutable record or review audit log. A git merge, code review approval, field missing from an archive, or AI-generated judgment does not establish the business authorization. Mark a case `NO AUTHENTIC APPROVAL` and exclude it from the human-validity denominator if the record does not exist. Do not turn this into `REVOKE`.

## Independent adjudication (before matcher execution)
Provide each human reviewer a blinded packet consisting of before/after source, associated finding, authentic approval provenance, validity period and policy scope. Mask any matching algorithm's predicted classification. Reviewers A and B must be two distinct eligible people: a policy/business authority reviewer and an independent source/KPI reviewer, or two qualified reviewers with logged expertise. Each records role (pseudonymized), decision, rationale, evidence location and time independently. If they disagree, record a third documented adjudication or documented consensus and preserve both initial labels. Never backfill names, approvals, or judgments with AI. `UNKNOWN` must remain a first-class result.

## Reference rule
- KEEP: an authenticated active approval covers the unchanged authority scope after the change, including the relevant evidence predicate and policy conditions.
- REVOKE: a documented cancellation, expiration, changed authorized finding/evidence scope, changed policy authority, or adjudicated source modification invalidates that approval.
- UNKNOWN: missing signature/status/scope, ambiguous source effect, uncertain equivalence, or reviewers unable to decide on the available evidence.

The strict source-file-hash rule in the archived LEAP governance specification remains a **candidate algorithm/reference policy**, not independently established human ground truth. Finite functional probes are another candidate, not proof of full equivalence.

## Analysis plan
1. Freeze and checksum approved source and decision records. Record source pairs and approval provenance before reference adjudication.
2. Adjudicate independently, retain initial and resolved outcomes. Count reference `UNKNOWN` and missing approvals separately.
3. Score candidate strategies on the **same approval/source-transition units**: strict file hash, code-representation fingerprint, unchanged source/finding identity, and bounded functional probe (when supported by the source language). Report invalid approvals retained, valid approvals revoked, true keeps, true revokes, unknowns, and method coverage. Do not assign accuracy to cases without approved references.
4. Cluster repeated transitions by approval ID and source-revision family; report per-cluster counts and paired errors. Avoid treating event-level downstream warnings as independent samples.
5. Use the frozen Paper 7 monitor only for consequent displayed-state propagation once externally adjudicated authority is known.
6. Interpret findings against research on static-analysis suppression evolution and warning identity, and state exact scope.

## Prospective scientific acceptance
A publishable empirical contribution requires a meaningful independently adjudicated corpus with source/approval evidence, diverse changes relevant to authority scope, a fair baseline comparison, a test set not used to design matchers, and a supported analysis of effects on displayed decisions. The number of available authentic cases is to be established, not invented. No fixed sample size or significance claim is assumed.

## Current gate state (2026-11-19)
Nine source-revision packets have original bytes and SHA-256 hashes. Zero authentic original business approvals are linked. Zero independent human authorization labels exist. Hence the primary authorization evaluation is **BLOCKED**, despite completed technical source comparisons.
