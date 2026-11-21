# Paper 7: independently executed research reproduction package

The complete temporal study reproduces from the supplied files: 4,935 traces, 26,430 events, six primary methods, SQLite and PyContract replays, thirty paired information witnesses, representation checks, 29 reference regressions, and four mapped Alertmanager expectations. All nine retained execution commands completed successfully. The independent scorer reproduced all 270 recorded primary metric rows directly from the raw JSONL outputs.

## Execute

Extract the ZIP and enter its `Paper7_Reproduction` directory. Use Python 3.11 or later with SQLite and pandas installed for that interpreter. The observed environment was Python 3.12.14, SQLite 3.53.1, pandas 2.2.3 on Linux x86-64. Every study-specific input and the pinned PyContract sources are bundled. The commands perform no network access or dependency installation.

```sh
python -B scripts/verify_package.py
python -B study/reproduce.py
python -B scripts/retain_replay.py study my_run
python -B scripts/independent_audit.py my_run my_analysis
```

The second command runs the original complete reproduction check in temporary storage. The third repeats it while retaining every generated prediction and command log in `my_run/`; use a fresh destination name for each run. The fourth independently recomputes the endpoint tables without importing the monitor, reference oracle, or original scoring helpers. It checks exact equality against all original metric rows and fails on any mismatch. Generated files do not change `study/`. Runtime fields vary across machines; raw prediction SHA-256 values are required to match exactly.

## Contents and results

| Location | Contents |
|---|---|
| `study/` | Unchanged extraction of the latest supplied offline supplement: policy, semantics, protocol and amendments, benchmark inputs, frozen references, code, upstream sources and licenses, historical expected outputs and hashes. |
| `saved_run/` | A fresh successful replay of that extraction, including all raw method predictions, PyContract engine audits, witness/hand-trace/malformed-input results, and nine numbered stdout/stderr logs in `fresh_execution/`. |
| `analysis/` | Independently recalculated denominators, all primary endpoints, base-only family/mechanism tables, one-row-per-trace design inventory and machine-readable audit. |
| `records/` | Source ZIP provenance, first documented-command exit status and logs, independent scoring stdout. |
| `scripts/` | The retained-execution wrapper, independent raw scorer and package-integrity verifier. |
| `DESIGN_AND_MECHANISMS.md` | Design counts, mechanism-to-data mapping and endpoint definitions. |

The held-out base analysis contains 987 traces and 5,286 events: 1,293 reference-active events, 3,993 reference-inactive events and 1,803 reference-UNKNOWN events. The complete held-out set has three variants of each base design, totalling 2,961 traces and 15,858 events. These transformations do not create additional independent designs. The full monitor has 987/987 base trace and episode agreement. The six methods preserve their outputs on all 3,290 metadata/time-unit transformation pairs. Both SQLite and PyContract reproduce all four reference fields on all 4,935 traces, with zero execution errors. The retained replay and independent scorer record these results separately.

`SOURCE_ARCHIVE.json` identifies the recovered supplement by SHA-256 `04f424b4b3bb9a4f867f2954b99345350dbb13a4b572d74898b530d762ff5339`. Its extraction was checked for safe paths and ZIP integrity. The original documented command succeeded in 13.29 seconds. A separate replay retained outputs in 15.69 seconds; all 58 original manifest entries verified and all nine subprocesses returned exit code zero. Times describe these executions, not comparative performance. The review was executed by an AI agent independently rescoring raw data; it is not human adjudication.

## Scope and limitations

The benchmark evaluates a newly specified governance-review lifecycle on constructed event sequences. It begins at the temporal observation interface. The supplied offline derivative removes 18,600 illustrative source-snapshot strings and their digests, which no evaluated temporal method consumes; its prediction digests equal the historical results. Private LEAP repositories, original source snapshots, manuscripts, personal records and the eleven-case private source-recovery replay are excluded. Re-execution of lexical adapters is outside this public-source-safe package. The generation design and all frozen temporal inputs are included; lexical source generation is not included. Python and pandas are environment prerequisites, not bundled executable runtimes. Paper 7 distribution authorization and its final license remain author decisions. The public upstream PyContract and Alertmanager files retain their Apache-2.0 licenses and provenance.
