# Paper 7 manuscript insertion text

## Methods: historical revision and authorization collection

The collection examined local project records and archived source revisions. The historical stratum comprised nine source-file transitions, represented by 18 before/after snapshots. Source bytes were checked against the supplied SHA-256 manifest and corresponding local Git objects. A separate stratum retained the recorded inventory and outputs of 24 constructed pilot cases. The two strata were analyzed separately.

The search covered 14,855 text and structured files, eight additional oversized files searched by streaming tools, and six tables across two SQLite databases opened in read-only mode. Exact paths, search expressions, revisions, queries, and checksums are retained in the evidence packet. Eighteen review slots were provided, corresponding to two reviewers for each historical transition. Initial decisions, signature references, and subsequent resolutions occupy separate fields.

## Results: collection and source verification

All 59 entries in the supplied input manifest passed checksum verification. All 18 historical source snapshots matched their corresponding local Git objects byte for byte. The search recovered three unsigned descriptive override texts; the inspected override and workflow ledgers supplied no authenticated business authorization record. No authorization could therefore be paired with a historical source transition in this collection. These observations concern the searched records and their documented coverage.

The delivered reviewer worksheet contains 18 unpopulated initial-decision fields. Consequently, there are zero paired initial decisions available for agreement analysis. Observed agreement, Cohen's kappa, KEEP/REVOKE frequencies, and authorization-retention accuracy are unestimated. Blank fields are retained as missing values, rather than recoded as UNKNOWN decisions. The 24 constructed pilot cases remain separate from these historical observations.

## Interpretation

This collection establishes the provenance and recoverability of the nine historical source transitions. Its recorded outcome is NO_AUTHENTIC_AUTHORIZATIONS_FOUND. Source verification and constructed-case outputs do not supply the missing reviewer decisions. The current manuscript can report the collection outcome and source-verification results; a completed reviewer-outcome analysis requires the populated decision records.

## Evidence locations

Historical transitions: collection_manifest.csv and verification/source_snapshot_checks.csv. Input integrity: verification/input_manifest_checks.csv. Search coverage: search_coverage.md and search/. Approval entries: authentic_approval_records.csv. Initial review instrument: adjudication_blind.csv. Analysis: manuscript_support/analysis/reviewer_analysis.json. Constructed cases: constructed_pilot/recorded_case_inventory.csv.
