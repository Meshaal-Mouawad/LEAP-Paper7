# Reproducibility audit

**Execution date:** 20 November 2026 (Asia/Riyadh). All commands below were run locally against files in this package. They are read-only on the frozen inputs unless stated otherwise. Source and benchmark experiments were preserved, not rerun.

| Operation / command | Exit | Observed result |
|---|---:|---|
| `unzip -l /Users/meshaalmouawad/Downloads/LEAP_Paper7_Formal_Contribution_Task_20261119.zip` | 0 | 13 archive entries including 12 listed input files. |
| `unzip -q /Users/meshaalmouawad/Downloads/LEAP_Paper7_Formal_Contribution_Task_20261119.zip -d /Users/meshaalmouawad/Downloads/LEAP_Paper7_Formal_Contribution_20261119` | 0 | Package extracted; current manuscript, source ZIP and evidence ZIP present. |
| SHA-256 and byte-size comparison of all rows in `CHECKSUMS_SHA256.csv` | 0 | 12/12 exact matches. |
| `unzip -t INPUTS/02_CURRENT_LATEX_SOURCE.zip` | 0 | No compressed-data errors. |
| `unzip -t INPUTS/03_FROZEN_SOURCE_TO_ALERT_EVIDENCE.zip` | 0 | No compressed-data errors. |
| Member-by-member SHA-256 comparison of `BASELINE_SOURCE/` with source ZIP | 0 | 16/16 extracted members byte-identical. |
| `python3 -B verify_preservation.py` in extracted integration root | 0 | `files_checked=347`, `unchanged=347`, `failures=[]`. |
| `python3 -B COUNTEREXAMPLES_AND_CHECKS/check_candidate.py` | 0 | Nine archived pair rows read; three constructed distinguishing witnesses; 14 temporal branch checks. It generated `results.json` outside the frozen evidence. |
| `python3 -B COUNTEREXAMPLES_AND_CHECKS/write_literature.py` | 0 | Generated 12 comparison rows in `CLOSEST_WORK_COMPARISON.csv` from manually checked primary-source records. This is a formatting utility, not a literature-search engine. |
| `pdfinfo INPUTS/01_CURRENT_MANUSCRIPT.pdf` | 0 | 30 pages, US letter. |
| `python3 -B build_package.py` | 0 | Built the final manifest and ZIP, checked every archived member against the local file, and verified the manifest. |
| Final SHA-256 manifest verification | 0 | Every listed output path passed size and SHA-256 comparison after package completion. |
| Final `unzip -t LEAP_Paper7_Formal_Contribution_20261119.zip` | 0 | No compressed-data errors after package completion. |
| Final ZIP entry/manifest comparison | 0 | ZIP contains exactly the package files other than itself; manifest lists exactly the package files other than itself and the manifest. |

The source PDF, all baseline LaTeX members, frozen integration records, original 252-stream results, historical 4,935-trace benchmark and author/declaration text were not modified. The mathematical checks are finite corroboration of candidate lemmas and monitor branches; universal claims rest on the written proofs. The new 12-source table distinguishes author full text from abstracts/exposed sections. No revised LaTeX build or rendered PDF inspection was executed because the manuscript revision gate failed.

## Completed checks

| Task completion item | Status | Evidence |
|---|---|---|
| Input identity and archive extraction | PASS | 12/12 input hashes, nested ZIP tests. |
| Empirical record and prior propositions preserved | PASS | 347/347 evidence files and 16/16 source members unchanged. |
| Formal quantifiers and assumptions | PASS | `FORMAL_DEFINITIONS.md`; T1–T4. |
| Complete proof and traceable witnesses | PASS | `FORMAL_THEOREM_AND_PROOFS.md`; `results.json`. |
| Necessary/sufficient and lower-bound logic | PASS | T1–T4 with explicit scope. |
| Decision and reason separated | PASS | `O_dec`/`O_full` and mismatch witness. |
| Strongest published predecessors checked | PASS | `CLOSEST_WORK_COMPARISON.csv` with passages/access levels. |
| Distinct consequential new theorem | FAIL | Antignac kernel ordering and OR example subsume the candidate. |
| Revised PDF synchronized | NOT VERIFIED | Gate excludes revision after FAIL. |
| Fixed review designation outside manuscript | PASS | Separate review file; no manuscript edit. |
| Archive integrity and final checksums | PASS | Final tests above. |

The ZIP is an out-of-band container for this directory. It excludes itself; otherwise archive construction would be recursive. `MANIFEST_SHA256.csv` excludes itself and the ZIP to avoid self-referential hashes, and covers every other delivered file, including original inputs and extracted copies.
