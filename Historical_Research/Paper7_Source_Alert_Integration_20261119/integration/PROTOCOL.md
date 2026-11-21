# Source-to-alert integration protocol

This protocol is written before the integration run. The unit is one of the nine ARCHIVED_REVISION file pairs. Existing endpoint records are consumed without rerunning or modifying earlier experiments. No constructed source controls are included.

## Mapping and technical reference

Calculation version = recorded executable-structure SHA-256 (Python AST; SQL/ABAP token screen). Documentation version = recorded deterministic generated candidate/detail SHA-256. These are representations, not proofs of numeric equivalence. Exact file = byte SHA-256. Dual context is the JSON pair [calculation hash, documentation hash]. The policy identifier is separate and never derived from a source or documentation change.

A uses byte identity as current context; B uses structure identity; C uses documentation identity; D uses the dual context. All use the same source pair and monitoring scenario. The technical reference for this experiment requires revalidation when either measured representation changes, and uses the frozen independent oracle on D's packets. This is an explicit choice of technical objective, not evidence that D is generally superior. False reset = A/B/C signals a context change while D does not; missed change = D signals a change while A/B/C does not. Counts are per pair and are not policy authorization errors.

E is an interface-preservation assay, orthogonal to A–D. On each A–D packet stream we encode actual three-, five-, six-comparison representations and decode to the unchanged frozen monitor. Six retains separate context/policy change and observation/suppression matches. Five joins suppression matches. Three joins current changes and each packet's matches, with the archived decoder convention of mapping all changes/mismatches to context. All retain presence, values, times, expiry, durations, severity. Five/six should retain reasons; three is required to preserve only state/activity/severity.

## Constructed monitoring inputs

The archived pairs contain no complete observed temporal monitoring histories. Therefore real operational alert decisions are unevaluable for all nine pairs. The following conditional technical scenarios supply explicitly constructed inputs; neither Boolean findings nor deferrals are inferred from source edits, output changes, merges, or approvals. Synthetic deferral packets exercise the monitor contract only.

Each pair is evaluated independently at t=0,2,3,5,7,9 seconds; before revision at 0,2 and after revision from 3. D=C=F=2 seconds; E=4 seconds; severity High. These parameters come from the frozen benchmark. Observation timestamps equal the current event time, so old-version evidence has a fresh time but retains its old binding. Findings are true before the revision. Seven scenarios: fresh positive; fresh negative after transition; positive observations bound to before-revision context after transition; positive observations with a before-revision deferral expiring at t=8; observations missing after transition; an independently constructed policy change at t=3 with fresh bindings; the same policy change with observations retaining old policy bindings. Deferral is supplied at all events of the deferral scenario with the before-revision context and policy and expiry 8. Policy otherwise stays p0. These scenarios are sensitivity probes, not independent real source cases or measured operational improvements.

## Outputs and checks

Export input packets and comparisons, per-event decisions, per-stream comparisons to the independent frozen oracle, per-strategy differences to D, pair-level change errors, actual-history availability, exact denominators. Verify five/six complete-output preservation and three decision preservation on every integrated stream. Confirm policy-only mismatch witnesses cause the expected three-comparison reason loss. Hash all consumed evidence and frozen executable modules. No old benchmark is rerun.
