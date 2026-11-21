# Paper 7 — R2 matched SQLite-runtime replication addendum

Prepared after the primary study, before executing this replication. This is a retrospective replication. It does not change the original protocol, held-out designation, sample, endpoints, or original frozen files.

## Purpose and method

Run the complete already-specified governance-episode policy on an established independently executing runtime: SQLite recursive SQL. The SQL implementation is newly written for this replication from `protocol/SEMANTICS.md` by AI agent `/root/alarm_semantics`. The agent did not inspect the tested monitor implementation. The same agent earlier authored the retrospective Python oracle; this replication adds runtime and implementation diversity rather than a third independent author.

The SQL handles event ordering, context/policy reset classification, evidence-quality precedence, freshness, qualification, activation, clearing, escalation, suppression binding, severity and reason emission. Python validates schema, normalizes time units, inserts data into SQLite, invokes SQL and scores outputs. No tested monitor or oracle is called. SQL uses a recursive common table expression with explicit phases per event. This is an external execution-runtime baseline, not an off-the-shelf runtime-verification framework or an industrial deployment.

## Frozen material and comparisons

Freeze this addendum, `monitor.sql`, `sqlite_baseline.py`, `run_replication.py`, the current semantics specification, benchmark policy, all 4,935 benchmark input traces and frozen references, 30 pair witnesses (60 sides) and their references, and the 21 valid hand-calculated trace references (post-evaluation v2 schema correction). Record hashes in FREEZE_R2.json before execution.

Execute identical trace inputs, policy and family severity. Primary replication outcome: complete-trace (state,active,severity) agreement with frozen reference. Also report all-field trace agreement, event tuple agreement, exact active-interval agreement, reasons/severity agreement, missed/unwarranted active decisions and execution failures. Aggregate overall, original split, family, mechanism and transformation variant. Witness agreement and hand-case agreement remain separate from 4,935 trace denominators. Validate 28 malformed schema cases with expected ValueError separately. Retain every prediction and any mismatch.

## Interpretation and amendment policy

Agreement demonstrates that the contract can be executed in an established SQL runtime with matched inputs. It cannot support an accuracy advantage over complete-contract conventional monitoring if results are equal. The replication is retrospective and same-specification; it does not add natural industrial observations or independently adjudicated policy validity. Do not claim comparative speed from elapsed execution time. It includes per-trace database construction and scoring.

If the frozen baseline fails, preserve initial outputs and issue a numbered corrective amendment before a rerun. Never overwrite the initial freeze or silently correct a scored baseline. A frozen implementation may be scored without claiming that its initial development was blinded to the already-known primary study conclusions.
