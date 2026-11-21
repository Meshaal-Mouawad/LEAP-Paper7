# LEAP Paper 7 formal-contribution research package

**Decision:** FAIL — no supported distinctive general formal advance. The complete proofs are in `FORMAL_THEOREM_AND_PROOFS.md`; the source/domain model is in `FORMAL_DEFINITIONS.md`; the closest-work and scientific judgments are in `CLOSEST_WORK_COMPARISON.csv` and `SCIENTIFIC_CONTRIBUTION_VERDICT.md`. The separate review is `INDEPENDENT_REVIEW_Elliot_Mercer.md`.

## Exact frozen sources

This folder contains unchanged extracted copies of `LEAP_Paper7_Formal_Contribution_Task_20261119.zip`. `CHECKSUMS_SHA256.csv` names and hashes all 12 top-level input files; all matched. The authoritative manuscript is `INPUTS/01_CURRENT_MANUSCRIPT.pdf`, 30 pages, SHA-256 `dfc3182803ea7a32892c2e2b83b00c70f27b84dd7991debcf896324a6b769e48`. The matching editable source is `INPUTS/02_CURRENT_LATEX_SOURCE.zip`, SHA-256 `6f6e88bdb810bb8ff2e67c6288ba81fabd33df0a2df75d4e662f34129b64df06`; its 16 extracted members are in `BASELINE_SOURCE/`. The frozen source-to-alert evidence is `INPUTS/03_FROZEN_SOURCE_TO_ALERT_EVIDENCE.zip`, SHA-256 `1caa7151eca5993bd0eea0043d7651055f71d43d14850a2ad481377d2bb68ac9`; its extracted tree is `FROZEN_EVIDENCE/Paper7_Source_Alert_Integration_20261119/`. No input was edited.

The actual archived source-pair classifications are in `FROZEN_EVIDENCE/Paper7_Source_Alert_Integration_20261119/integration/outputs/pair_categories.csv`; complete original stream decisions are in the adjacent `decision_events.csv` and `RESULTS.md`. `COUNTEREXAMPLES_AND_CHECKS/results.json` contains **new constructed checks** and labels them separately from the archived pair IDs. The preservation checker reports 347/347 files unchanged.

## Inspect and reproduce

From this package root:

```sh
python3 -B COUNTEREXAMPLES_AND_CHECKS/check_candidate.py
python3 -B FROZEN_EVIDENCE/Paper7_Source_Alert_Integration_20261119/verify_preservation.py
python3 - <<'PY'
import csv,hashlib,pathlib
root=pathlib.Path('.')
for r in csv.DictReader(open('MANIFEST_SHA256.csv')):
 p=root/r['path']; assert p.stat().st_size==int(r['bytes']); assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
print('manifest verified')
PY
```

To rebuild the complete archive and manifest, run `python3 -B build_package.py` from this directory. The ZIP contains the directory under its fixed name and excludes itself; the manifest covers every other file except itself.

The first check prints 9 archived pair rows, 3 witness pairs and 14 temporal checks; it rewrites only its own `results.json` deterministically. The second reads the frozen preservation manifest. The final command verifies every delivered file. The 252 completed strategy streams and the historical 4,935-trace benchmark are not re-executed by these commands.

## Manuscript decision

`FINAL_MANUSCRIPT/UNCHANGED_BASELINE.md` identifies the unchanged PDF and LaTeX source. A new `Paper7.tex` and `Paper7.pdf` are absent because the task allows manuscript integration only after a PASS; the proof and novelty gate yielded FAIL. Existing author information, five proof environments, figures, bibliography, empirical data and reference methods remain in the preserved inputs.
