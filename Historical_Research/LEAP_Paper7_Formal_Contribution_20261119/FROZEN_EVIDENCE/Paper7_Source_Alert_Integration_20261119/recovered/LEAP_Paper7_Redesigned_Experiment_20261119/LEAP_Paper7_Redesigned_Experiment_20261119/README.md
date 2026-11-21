# LEAP Paper 7 — Reconstructed technical experiment

This package replaces the rejected authorization-judgment experiment with a fixed-input comparison of two independently observable technical outputs across archived Git source revisions: executable KPI behavior and offline LEAP KPI extraction/detail fields.

**Execute:** `python -B run_experiment.py`

**Inputs:** `cases/P7R01`–`cases/P7R09` (byte-verified archived before/after source files), `case_manifest.csv`, and the fixed offline parser/detail engine under `src/`.

**Outputs:** See `outputs/summary.json`, `outputs/paired_endpoints.csv`, `outputs/version_transition_events.csv`, and `outputs/all_case_details.json`.

**Research documentation:** `EXPERIMENT_PROTOCOL.md` and `RESULTS_AND_DECISION.md`.

Two constructed controls are labelled `CTRL_DOC` and `CTRL_CODE` and remain outside the observed nine-case counts. No reviewer decisions are required by this experiment.

**Study status:** technical experiment reproduced; manuscript remains on scientific hold pending integration and contribution verification.
