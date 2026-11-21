# R3 — authentic PyContract monitoring baseline

Retrospective addendum, prepared before scored execution. Original Paper 7 frozen inputs and results remain unchanged.

## Why this baseline

PyContract is an established event-stream monitoring and runtime-verification library introduced by Dennis Dams, Klaus Havelund and Sean Kauffman, *A Python Library for Trace Analysis*, RV 2022, LNCS 13498, pp. 264–273, DOI 10.1007/978-3-031-17196-3_15. The official implementation is `https://github.com/pyrv/pycontract`. Its internal DSL implements parameterized states and event-triggered state transitions. Temporal guards can inspect event timestamps. This fits Paper 7's recorded-event semantics.

Pinned upstream commit: `e378eed38699bcff33e2ae71426e6b161690cdfa`. Upstream README calls this version 1.3.2; pyproject packaging metadata says 0.1.0, so commit and file hashes are authoritative version identifiers. Nine fetched files match their pinned Git blob identities exactly. Apache-2.0 license and all fetched source notices are preserved. No upstream files are modified.

## Actual execution and matched scope

`pycontract_baseline.py` expresses the full policy as a PyContract Monitor with four data-state classes: Dormant, Qualifying, Raised, Recovering. The authentic upstream engine's Monitor.eval, eval_states and State.eval dispatch each input event and retain/replace data states. The monitor's guards implement version/quality/freshness requirements and its transitions implement dwell, clearing and escalation clocks. Suppression is a presentation overlay. These guards are the study-specific specification, as expected for an internal monitoring DSL.

Python preprocessing only checks schema and converts time units; it does not calculate lifecycle outputs. No LEAP monitor, reference oracle or SQL baseline is imported or called. The engine receives identical normalized evidence and policy to the primary study. All 4,935 original traces, all families and transformations are included. Outputs use identical state, active, severity and reason fields. Finite traces invoke Monitor.end; no eventual-clearing requirement is added because the study allows active episodes at the end. Each trace records authentic engine event count, state-transition count and concrete PyContract state-class sequence.

The author is separate AI agent `/root/alarm_semantics`, who previously authored the Python reference and SQL replication and has not inspected the main monitor. Independent engine code provides an established monitoring implementation; study-specific policy encoding is not a third independent human specification.

## Freeze and endpoints

Before scored evaluation, freeze this protocol, policy encoding, driver, upstream source files, original semantics/policy/benchmark/reference files and corrected hand-case reference file. Primary endpoint: complete-trace (state,active,severity) agreement. Secondary endpoints: event agreement, missed/unwarranted active outcomes, exact active-interval agreement, reasons, severity and execution failures. Preserve all predictions and exceptions; do not exclude failures. Report original development and held-out subsets as retrospective replays. Separately run 60 witness sides, 21 hand-calculated valid cases and 28 malformed-input ValueError cases.

An upstream unmodified demonstration was executed before this freeze and reported its three designed command-lifecycle errors. A five-event development smoke trace verified actual state-class changes. These are development checks, not benchmark scores. No scored baseline results were inspected before freezing.

## Interpretation and limits

The comparison tests whether an established monitoring engine supplied with the complete policy and context reproduces the reference. Equality means the contribution is the evidence/version contract and its analysis, not a new monitoring engine or superiority to fully informed temporal monitoring. This run is retrospective and uses the same synthetic traces. No physical alarm behavior, independent industrial deployment, continuous-time polling, background deadlines, parameter learning or latency superiority is claimed. PyContract is executed offline; no live service or monitoring infrastructure is contacted. Real-time properties are evaluated only when recorded events arrive. Missing external requirements are not manufactured.
