# LEAP Paper 7 — Source-revision authorization scientific gate (2026-11-19)

**Status: controlled technical research pilot complete; authentic human authorization reference NOT AVAILABLE. Paper 7 submission held.**

## Reproduce without external connections

Run from the extracted package root:

```sh
python research/run_pilot.py
```

Python 3.12+ standard library; requires neither network nor extra packages. This replays the archived function-level authorization checks, 24-case source-revision experiment, and downstream frozen-monitor propagation. The monitor ZIP is automatically extracted if necessary. The first line of the runner verifies `research/pre_registered_protocol.json` against its frozen SHA256.

## What is measured

- `analysis/native_override_test_results.json`: 10 selected unit-level calls to two AST-extracted native LEAP override functions, evaluated against the archived governance docs; 4 conform and 6 do not.
- `analysis/proxy_case_records.json`, `proxy_summary.json`, `proxy_predictions.csv`: 24 intentionally constructed before/after code pairs (four KPI families), reference outputs from a declared finite input grid, compared with four carry-forward matchers.
- `analysis/downstream_monitor_bridge.csv`, `downstream_bridge_summary.json`: 24 x 4 *deterministic* carry-forward choices mapped onto the frozen Paper 7 12-event sample; not 96 independently observed users or warnings.
- `analysis/natural_revision_*`, `analysis/historical_override_*`: original supplied LEAP Git history reads. Their source command scripts are included, but rerunning historical scan requires the **original 169 MB LEAP Git archive** separately supplied in this project; the package deliberately excludes bulky `.git` objects.
- `research/Independent_Authorization_Reference_Schema.csv` and `...Instructions.md`: empty instrument for actual human adjudications. It deliberately contains no invented approvals.
- `preserved/`: original 25-page scientific baseline PDF; paper's separate frozen reproduction ZIP in `inputs/` remains unchanged.

## Scientific interpretation

Archived main approval ledgers have zero entries. Historical branches contain three unsigned override text entries lacking authentic approver/status/time. They cannot establish whether changed evidence is legitimately authorized. The source-output comparison's KEEP/REVOKE labels are bounded laboratory proxies; a file-hash revocation under native strict governance can be compliant even when the full-grid output proxy says equivalent. The exact event source-witness is reproduced by its original frozen monitor, not an independently collected operational record.

## Publication decision

The controlled pilot establishes precise software-conformance defects and matcher trade-offs, **not** general operational validity or a verified authorizable source-equivalence rule. Do not mark Paper 7 scientifically complete or upload it for journal review until independently adjudicated source/approval transitions and substantive novelty against established source-evolution literature are verified.

For full details see `reports/Scientific_Gate_Report_20261119.pdf` and the provisional, explicitly unsubmitted thesis in `manuscript/`.
