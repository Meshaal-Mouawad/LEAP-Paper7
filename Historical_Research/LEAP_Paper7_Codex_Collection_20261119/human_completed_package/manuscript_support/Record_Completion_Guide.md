# Completing the review records

For each reviewed transition, record the reviewer's original KEEP, REVOKE, or UNKNOWN decision in adjudication_blind.csv, together with the actual decision time, reason, and manual-signature reference. Preserve the initial decision when recording a disagreement or resolution. Keep reviewer codes R1 and R2 pseudonymous.

For recovered approvals, populate authentic_approval_records.csv from the original record, retaining its original status, approver role, time, finding, scope, source revision, policy version, expiry or revocation, exact evidence locator, and checksum. Missing values remain blank or UNKNOWN as appropriate.

Then run from the package directory:

    python -B analyze_reviewer_records.py --packet . --output completed_review_analysis

The script preserves supplied labels, checks the review record fields, reports paired initial agreement, and calculates three-category Cohen's kappa when defined. It does not generate decisions. Provide the populated files and corresponding source evidence for the final manuscript analysis.
