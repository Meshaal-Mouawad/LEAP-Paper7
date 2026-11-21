# LEAP Paper 7 — Dual-Endpoint Source-Revision Experiment

**Study type:** Retrospective, fixed-input technical experiment on archived source revisions.

**Purpose:** Determine whether a source revision changes executable KPI behavior, LEAP-extracted KPI documentation, both, or neither. Establish which version-comparison signals would trigger output-specific technical revalidation. The unit of analysis is an archived before/after file pair.

## Research questions

**RQ1.** Do archived revisions exist for which fixed-fixture execution results are preserved but LEAP-generated KPI candidate/detail records change?

**RQ2.** Do archived revisions exist for which executable behavior changes but LEAP-generated KPI candidate/detail records remain the same?

**RQ3.** What distinctions do exact-file, executable-structure and generated-detail signatures make across the same revision pairs?

## Evidence basis and selection

Nine original before/after source snapshots were extracted from the read-only Codex evidence archive, which supplied commit identities, paths and SHA-256 hashes. The nine pairs cover four distinct Git transitions and examples in Python, SQL/TSQL and ABAP. Every snapshot is verified byte-for-byte against the original manifest. All nine supplied pairs are included; none were selected based on output.

Two additional controlled cases are derived from archived Python example P7R08 and are explicitly separate from observed revisions. One changes the formula comment without changing executable code; the other changes a multiplication constant without changing the formula comment. These controls test whether the experiment detects each output channel independently.

## Fixed comparison procedure

1. **File identity:** Compute SHA-256 over original source bytes. Different hashes indicate a file revision, irrespective of consequence.
2. **Executable structure:** For Python, hash the normalized syntax tree without source-location attributes. For SQL/TSQL and ABAP, compare comment-stripped, whitespace-normalized tokens. Token-based comparisons are structural screens and are not proofs of program equivalence.
3. **Execution observations:** Run Python examples in isolated subprocesses using fixed inputs. Run SQL/TSQL fragments against fixed, in-memory SQLite fixtures. Record output columns, values, errors and unsupported cases. Preserve SQL dialect and input-binding restrictions in the outcome classification.
4. **Documentation observations:** Run the archived LEAP KPI extractor and deterministic detail engine offline on each original source snapshot. Compare the multiset of extracted KPI names and eight generated detail fields, excluding source-line coordinates. Record exact generated values and SHA-256 signatures.
5. **Output-specific flags:** Compare structure and generated-detail signatures separately. The joint signal indicates that at least one measured channel changed. Export all before/after hashes as transition events for later integration with Paper 7's monitor.
6. **Controls:** Independently verify comment-only and computation-only perturbations. The respective unaffected output channel must remain equal.

The experiment operates without remote model calls, deployment credentials, approval labels or reviewer judgments. The offline parser snapshot has one local variable and its comment renamed without changing behavior; equivalence with the original parser was checked on all 18 historical snapshots.

## Primary outcomes

- Number of observed revisions changing the executable-structure signature.
- Number changing generated KPI candidate/detail output.
- Number changing either channel.
- Execution-result agreement among pairs with comparable executable fixtures.
- Cases where the two output channels disagree on whether a revision changed their observed outputs.

These are descriptive counts over the fixed archived set; no population-level inference or accuracy claim is made from them.

## Reproduction

From the extracted experiment directory:

```bash
python -B run_experiment.py
```

The code uses Python 3.10+ and standard-library modules. Outputs are written to `outputs/paired_endpoints.csv`, `outputs/version_transition_events.csv`, `outputs/all_case_details.json` and `outputs/summary.json`.

## Limitations

The source files are archived sample programs, and nine pairs come from four distinct transitions. SQLite executes a compatible subset of the archived SQL/TSQL sources; one TSQL fragment has unresolved input bindings and one ABAP example has no available runtime. The executable comparisons use fixed input fixtures and establish agreement only for those fixtures. The LEAP documentation endpoint consists of offline candidate and detail fields, not a complete rendered Bluebook. This experiment does not evaluate production warning outcomes or decisions about earlier review deferrals. Those require a separate evidence-to-decision integration study.
