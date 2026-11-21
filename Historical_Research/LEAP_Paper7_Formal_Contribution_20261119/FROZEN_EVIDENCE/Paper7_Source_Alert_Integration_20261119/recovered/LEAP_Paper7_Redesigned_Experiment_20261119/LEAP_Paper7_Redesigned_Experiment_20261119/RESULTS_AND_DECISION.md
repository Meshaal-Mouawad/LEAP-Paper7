# Paper 7 — Executed Dual-Endpoint Revision Study

**Decision:** The redesigned technical experiment is executed and reproducible. The source-revision evidence now distinguishes executable structure from extracted KPI documentation. Paper 7's publication-level contribution gate remains open pending a tested bridge to governance-alert decisions and closest-work novelty verification.

## Why this experiment was redesigned

The earlier protocol treated a source diff as the basis for a decision about the validity of an earlier authorization. The archived evidence contains source revisions but no complete authorization records. The new protocol asks a question that those records can answer: what technical outputs actually change when code and its source-linked documentation evolve?

This test is aligned with LEAP's purpose. LEAP extracts KPI names and formula-related details from code and accompanying comments. A comment-only revision can therefore change the documented business meaning while leaving the executable calculation unchanged. A code-only revision can change a calculation while leaving a formula comment unchanged. These different outcomes demand different version-comparison signals.

## Results from archived Git revisions

| Case | Executable structure changed? | Extracted KPI documentation changed? | Fixed-input execution | Interpretation |
|---|---|---|---|---|
| P7R01 | No | Yes | ABAP runtime unavailable | Documented KPI inventory changes |
| P7R02 | No | Yes | Same | Formula disclosure added to source comments |
| P7R03 | Yes | Yes | Different | KPI source replaced by a different calculation |
| P7R04 | No | Yes | Same | Formula wording and extracted fields change |
| P7R05 | No | Yes | Same | Documented name/formula introduced |
| P7R06 | No | No | Same | File representation changed without measured output change |
| P7R07 | Yes | Yes | Unresolved input bindings | On-spec formula replaced by a catalyst-cost fragment |
| P7R08 | No | No | Same | Python formatting revision |
| P7R09 | Yes | No | Different | Standalone input definitions added; prior source raises `NameError` |

**Observed changes:** All nine source files have different byte hashes. Three change executable structure. Six change extracted KPI documentation. Seven change at least one of these outputs. Two change neither measured output despite changed file bytes.

**Comparable execution:** Eight source pairs were attempted. Seven yield comparable execution observations: five unchanged and two different. One SQL fragment lacks input bindings in the fixed SQLite fixture. The ABAP source is assessed statically.

**Central observation:** Among five pairs with preserved execution observations, three change LEAP's extracted KPI candidate or detail records (P7R02, P7R04 and P7R05). Conversely, P7R09 changes standalone execution status while leaving the selected extracted detail fields unchanged.

## Controlled discrimination tests

| Controlled perturbation | Executable structure | LEAP documentation output | Execution observations | Result |
|---|---|---|---|---|
| Formula comment changed from multiplier 24 to 25 | Same | Changed | Same | PASS |
| Executable multiplier changed from 24 to 25; comment retained | Changed | Same | Different | PASS |

Both controls use the original archived P7R08 sample as the fixed base and are kept separate from the nine historical revisions.

## What the results establish

**Technical implication:** A code-only source revision signature does not preserve all generated documentation fields. A documentation-only signature does not preserve all executable changes. An exact-file signature detects both but triggers revalidation for two revisions that leave the measured outputs unchanged. Output-specific signatures can express these different technical needs explicitly.

**Paper 7 integration:** `outputs/version_transition_events.csv` records the observed code and documentation changes for each source pair. These are suitable inputs for a subsequent test of evidence-context versioning under the frozen governance-alert monitor. The technical outcome demonstrated here is the need to distinguish the source evidence channels, not a conclusion about the continuing authority of a deferral.

## Verification record

- All 18 archived source snapshots matched the read-only collection's SHA-256 hashes.
- The fixed extractor's naming-only source adjustment reproduced the original parser's outputs on all 18 historical snapshots.
- All nine cases and both separate controls completed.
- Control assertions passed.
- The study was executed twice with identical machine-readable results; the extracted final package reproduces them without external services.

## Scientific decision

**EXPERIMENT COMPLETE — PAPER 7 STILL ON SCIENTIFIC HOLD.** The dual-endpoint evidence provides a real, reproducible source-revision phenomenon and a technical input for the existing version-monitor model. A paper-level claim requires a demonstrated contribution beyond existing abstraction and source-documentation research, including the connection from dual-output source changes to specified alert decisions.

## Limitations

The sample files were collected from developer archives rather than a randomly selected enterprise corpus; some pairs share source ancestry. The execution checks use fixed fixtures, not exhaustive semantic equivalence. The documentation checks use the deterministic offline extractor and detail engine, with generated name/field comparisons rather than complete publishing-page reproduction. One SQL/TSQL fragment lacks required input bindings and one ABAP source was not executed. The experiment measures technical output differences across source revisions and does not provide an authorization reference or measure operational consequences.
