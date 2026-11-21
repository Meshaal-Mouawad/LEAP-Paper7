# LEAP Paper 7 — Source-Revision Authorization Scientific Gate

**Research assessment | 19 November 2026 | Intended journal: *Science of Computer Programming***

## Scientific decision

**A source-grounded, reproducible implementation defect has been established, and controlled comparison experiments demonstrate distinct failure modes of four authorization-carry-forward strategies. The broader submission contribution is not yet established.** In the archived LEAP implementation, signed source evidence, approval status and review-field application are handled by the definition-override code. Ten controlled calls to that exact archived code yielded six decisions inconsistent with the separately recorded governance rules. A second test, involving 24 controlled source-revision comparisons from four archived KPI families, demonstrated different false-retention and false-revocation counts under a fixed, independently specified output-reference grid. No authentic human approval transition was available to determine whether the reference decisions reflect organizational authorization.

**Decision: NOT SCIENTIFICALLY READY FOR JOURNAL SUBMISSION.** The next scientific gate was executed as far as the records permit. Original Paper 7 remains frozen; the new results are issued as a reproducible research pilot, not as a completed new publication.

## 1. The practical problem and the research object

A key performance indicator (KPI) is a calculation used to describe an operational quantity. An organization's automated documentation tool can extract that calculation from SQL or Python and present a proposed formula with source provenance and a review status. **LEAP—Literate Programming for Automated KPI Extraction**—implements that source-linked workflow. A business owner may approve a documentation override, and the system must determine whether the approval is still applicable after the source evidence changes. The issue is consequential because applying an old approval to changed evidence can conceal a required review, whereas discarding a still-relevant approval creates review work.

This assessment directly inspected the supplied LEAP Git archive, the specification in `.ai/GOVERNANCE_SPEC.md`, the rules in `.ai/BUSINESS_RULES.md`, and the definition-override functions in `bluebook_generator/main.py`. It separately used Paper 7's frozen monitor to check how a carry-forward decision affects the displayed warning. **The authorization-reference source is the pre-existing governance documentation**, not the monitor being compared.

The specification says to track source identity and `code_hash`, flag drift, and accept a human override only when KPI identity and source hash match. The business rules also describe approval status `APPROVED_BY_BUSINESS` and source file signatures. These rules give a clear, testable *strict source-bound* approval criterion. They do not by themselves define business-approved semantic equivalence across distinct code contents.

## 2. Archived implementation conformance

The original function `_apply_definition_override()` obtains an optional `file_signature` from the override and `source_file_signature` from the KPI record. Its guard rejects a mismatch **only if the override signature is nonempty**. The function then applies approved-field values before checking the override's recorded status. A read-only search of the tracked Python source found `source_file_signature` at its read site in `main.py` and found no assignment to that field within the tracked Python files.

The test harness compiled only two exact AST-selected functions from the archived `bluebook_generator/main.py`, using controlled input dictionaries; it did not execute the full application or modify the archive. The reference for each case followed the documented status and signature requirements. All results can be rerun using `python research/audit_native_override.py`.

| Controlled call | Documented reference | Archived code behavior | Finding |
|---|---|---|---|
| Approved, signed, matching source | Apply | Applied | Conforms |
| Approved, signed, changed source | Withhold | Withheld | Conforms |
| Approved, **unsigned**, changed source | Withhold | **Applied fields** | Source-binding mismatch |
| Approved, unsigned, unchanged source | Withhold pending verifiable signature | **Applied fields** | Missing-signature acceptance |
| Pending status, matching signature | Withhold | **Applied fields** | Status not enforced at field-application stage |
| Rejected status, matching signature | Withhold | **Applied fields** | Status not enforced at field-application stage |
| Approved, source actually unchanged but signature field absent | Eligible if evidence supplied | Withheld | Missing-source-metadata integration gap |
| Approved, matching `code_hash` supplied without expected signature field | Eligible under code-hash wording if connected | Withheld | Identity-field mismatch |
| No override ledger entry | Withhold | Withheld | Conforms |
| Approval for a different KPI name | Withhold | Withheld | Conforms |

**Observed: four conforming and six nonconforming cases among ten intentionally selected test conditions.** This is a software conformance result, not an estimated operational failure frequency. For `PENDING` and `REJECTED`, the code modifies candidate definition fields; later display-state logic separately checks for `APPROVED_BY_BUSINESS`, so the finding concerns field integrity rather than a demonstrated invisible production warning.

The three approval stores present on archived `main`—`kb/overrides.json`, `bluebook_generator/kb/overrides.json` and `docs/governance_overrides.json`—contain **zero recorded entries**. A wider scan of all **156 archived Git commits** found one nonempty version of `docs/overrides.json`, retained in 41 branch commits, with three historical business-definition entries. Those records have no approver, explicit approval status, signed source identity, approval date or recorded expiry. They **cannot be treated as independently authorized deferrals**. The older branch file was not silently combined with the present main-branch application to invent an observed runtime outcome.

## 3. A separate, controlled source-revision comparison

The second experiment tests a different scientific question: **How do alternative matching strategies behave when the same KPI calculation is changed, and reference equivalence is assessed by actual outputs on an explicit audit domain?** This is a bounded computational proxy. Its oracle is separate from the compared matchers: an independent full-input execution grid fixed in `pre_registered_protocol.json` before the methods were run. SQL expressions were executed with SQLite; Python functions were executed in isolation from the archived source, using exact fixed inputs. The candidate behavioral matcher received only a smaller prespecified input subset.

The four families are *yield rate* (SQL), *asset utilization* (SQL), *daily throughput* (Python), and *emissions intensity* (Python). Of the 24 source pairs, some use unmodified archived correct/incorrect source files; the others introduce explicitly labeled controlled changes such as comments, spacing, local-variable renaming, altered operators, and branches triggered only at test inputs omitted from the candidate's small probe set. The SQL source files contain archived trailing Markdown fences; these are removed solely from a temporary execution view, while original file hashes remain unchanged.

The reference says `KEEP` when both versions produce equal outputs throughout the full declared input grid and `REVOKE` when any comparison differs. This is **finite-grid output equivalence**, used only as a technical proxy for a hypothetical scope-limited approval. It does not establish actual human permission to carry an approval forward. Four alternatives were applied to all 24 cases: raw source-file hash equality; unchanged KPI identity/presence; normalized SQL or Python AST fingerprint; and equality of the small probe-output vector.

| Strategy | Equivalent cases retained | Different cases retained (false carry-forward) | Equivalent cases revoked (false re-review) | Different cases revoked |
|---|---:|---:|---:|---:|
| Exact file SHA-256 | 4 | **0** | **10** | 10 |
| KPI identity/presence only | 14 | **10** | **0** | 0 |
| Syntax fingerprint | 9 | **0** | **5** | 10 |
| Small behavioral probe | 14 | **4** | **0** | 6 |

There were **14 output-equivalent cases and 10 different-output cases on the full audit grid**. Raw hashing rejects all ten equivalent-but-text-changed cases under the proxy criterion. Identity-only matching retains all ten changed-behavior cases. Syntax-based fingerprinting rejects five valid equivalent cases, including changes in algebraic expression or local variable names. The small behavioral probe misses four changes activated only at the full reference grid's excluded inputs (a denominator of 37, a duration of 13 hours, or exported energy equal to 1, according to the relevant source family).

These observations establish two technical requirements for future authorization research: the evidence-equivalence test must specify which output semantics the approval concerns, and limited behavioral agreement must record uncertainty for untested conditions. **Neither output-grid equivalence nor file-hash equivalence is a verified business authority rule.** The native LEAP specification uses strict source identity, so the ten hash-based revocations are *correct under the native rule* and are false revocations only under the different, explicitly declared semantic proxy.

## 4. Consequence for reviewer-facing decisions

The new source-authorization outcomes were propagated through the unchanged frozen Paper 7 monitor using the same 12-event constructed audit trace. Its three-second event is a positive finding that has already qualified an active episode, with an old deferral still nominally within its expiry window. Holding all time, observation, policy and finding inputs fixed, only the assumed applicability of the deferral changes:

| Reference applicability | Time 3 s displayed state | Episode active | Severity | Reason |
|---|---|---|---|---|
| `KEEP`: authorization still covers current evidence | `SUPPRESSED` | true | `NONE` | `SUPPRESSION` |
| `REVOKE`: authorization no longer covers current evidence | `ACTIVE` | true | `COMPLIANCE_AUDIT_GAP` | `STATE` |

Across the 24 controlled source comparisons, each wrong carry-forward decision produced one wrong displayed-decision event in this fixed trace. The resulting numbers were 10 affected constructed cases for exact hashing, 10 for identity-only matching, five for syntax fingerprinting, and four for sparse behavioral matching; **episode-activity disagreement remained zero for every strategy**. The event differences are deterministic propagation of the previously classified authorization outcomes, **not** independent validation observations or additional real-world traces.

The original Paper 7 finding remains preserved: omitting suppression-version checking alters complete decisions on 30 of 987 held-out base traces, equivalent to ten temporal designs repeated in three held-out rule families, while preserving all 987 episode-activity sequences. These figures continue to describe the constructed monitoring contract.

## 5. Actual source-history availability

The preserved main branch has 28 commits and 27 adjacent first-parent revision pairs. Seven original KPI examples were each present on 25 adjacent pairs; **none of these seven KPI source files changed across those eligible pairs**. The nine originally reported Python/SQL/TSQL-changing commit pairs include application or development-code changes and initial import rather than longitudinal revisions of these seven KPI calculations. No historical record connects an approved deferral to a before/after source revision and independently establishes its continued authority.

A larger scan inspected all 156 archived commits, including branches, and found the three aforementioned historical text overrides. Their absence of signed approvals and authorizing decision history is recorded, rather than assigning assumed human verdicts. A blank `Independent_Authorization_Reference_Schema.csv` and an adjudication protocol are included in the package to preserve the distinction between *observed approval*, *source-diff evidence*, *controlled proxy*, and *unknown*.

## 6. Where the research frontier stands

The earliest parts of the original novelty argument are established prior knowledge. The 2025 FSE study by **Hu, Wang, Rubin and Pradel** examined 7,357 suppressed static-analysis warnings in 46 Python projects and reported that some suppressions unintentionally hide later warnings. The paper investigated suppression use and evolution empirically (DOI [10.1145/3715729](https://doi.org/10.1145/3715729), full text inspected, including results and limitations). **Li and Yang's** 2024 IEEE TSE study manually labeled 3,451 warnings across more than 2,000 commits and developed a better warning-tracking method (DOI [10.1109/TSE.2024.3358283](https://doi.org/10.1109/TSE.2024.3358283), full text and methods inspected). These results establish that both suppression evolution and cross-revision warning identity are active, empirically developed areas.

**Gröninger, Souza and Pradel** (2025) compared code behavior across changes using learning-guided execution and evaluated against 224 manually annotated Python changes (DOI [10.1145/3715760](https://doi.org/10.1145/3715760), publisher abstract inspected). **Guan and Legunsen** (ICSE 2025) evaluated change-aware runtime verification on 2,028 revisions of 66 projects (DOI [10.1109/ICSE55347.2025.00099](https://doi.org/10.1109/ICSE55347.2025.00099), full text introduction and evaluation description inspected). They establish important neighboring methods for change-sensitive behavior and instrumentation.

The **OASIS SARIF 2.1.0 specification** already represents external suppressions with `accepted`, `underReview`, and `rejected` statuses, and supports source-result fingerprints ([OASIS specification](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html), relevant sections inspected). **Prometheus Alertmanager** already separates active alerts from delivery silences ([official documentation](https://prometheus.io/docs/alerting/latest/alertmanager/)). These mechanisms must receive explicit credit in Paper 7's scientific framing.

**Residual research question:** For an authenticated, source-bound *human authorization*, how should a changed finding be matched to its earlier evidential scope, and how accurately can source-change comparators distinguish valid carry-forward from obsolete approval? The target becomes a measurable authority-matching problem, not the general fact that warnings can be suppressed or that output information can be reduced.

## 7. Decision on manuscript reconstruction

**The source-based pilot is complete; full publication reconstruction is held.** The experiments establish reproducible LEAP code defects and meaningful controlled trade-offs. Their reference decisions are derived from a documented strict source-hash rule or from deliberately bounded output equivalence, **not from externally authenticated business review decisions**. The native historical ledgers do not supply that decisive scientific evidence. Rebuilding the submitted paper as if this pilot established the correctness of human deferral transfer would repeat the original contribution error.

The next manuscript's defensible scientific question is stated as follows:

> **When source evidence changes, which source- and approval-scoped conditions justify retaining a previously authorized governance deferral, and how do alternative matchers affect displayed decision accuracy against independently adjudicated authorization outcomes?**

The existing five-comparison theorem, frozen monitoring oracle, and exact obsolete-deferral trace can become the downstream correctness machinery. The new source-revision reference must be the primary independent observation. The existing Q3 metadata and milliseconds transformations should remain technical robustness checks, rather than the central research question.

An executable, prospective reference instrument is provided. Each record must include the source pair, original finding, authentic approval identity and status, approver, policy version, expiry, relevant change evidence and two independently recorded adjudications. `UNKNOWN` is a legitimate reference outcome and must not be silently converted to KEEP or REVOKE. Collect genuinely source-changing cases and distinct repositories or change families, then compare algorithms against these adjudicated references with clustered reporting. The original experimental data, figures and theory remain frozen.

## 8. Gate verdicts

| Scientific release gate | Decision | Evidence |
|---|---|---|
| Source and policy provenance | **PASS** | Archived Git specifications and selected code functions hashed and retained |
| Native implementation conformance assessment | **PASS** | Ten controlled calls, six code/spec discrepancies, exact executable harness |
| Controlled strategy comparison | **PASS** | Twenty-four cases, four families, prespecified grids and reproduced confusion counts |
| Downstream monitor propagation | **PASS** | Frozen monitor replay, 24 cases × four strategies, active flag preserved |
| Natural source-revision evidence | **PARTIAL** | 27 adjacent main-branch pairs; seven KPI examples unchanged across eligible pairs |
| Authentic independently adjudicated authorization labels | **FAIL** | No approval identity or decision history in available records |
| Novel consequential contribution beyond the closest published work | **NOT VERIFIED** | Case-study defect is established; transfer across real approval decisions remains untested |
| Reader-first revised paper | **NOT RUN** | Scientific authority reference remains unresolved; previous rejected manuscript preserved |
| SCP submission release | **FAIL** | The material scientific reference gate has not passed |

## 9. Reproducibility and file provenance

Run the enclosed `research/run_pilot.py` using Python 3.12 or later. It checks the fixed protocol SHA-256, independently executes the selected historical override functions, runs SQL in an in-memory SQLite database, executes only the isolated original Python KPI functions on fixed data, evaluates the four strategies, then propagates their decisions through the unchanged frozen Paper 7 monitor. It verifies the expected counts. The original 169 MB LEAP archive is required only to repeat the full Git-history discovery; hashed source snapshots are included so the controlled tests can be rerun without that large archive. All controlled source changes are recorded with before/after hashes.

The script outputs are in `analysis/native_override_test_results.json`, `analysis/proxy_case_records.json`, `analysis/proxy_summary.json`, `analysis/natural_revision_summary.json`, `analysis/historical_override_discovery.json`, and `analysis/downstream_bridge_summary.json`. The baseline manuscript and frozen research ZIP remain unchanged. No existing external repository or author-approved record was modified.

## Limitations

The source-revision comparisons are purposive controlled pairs derived from four archived KPI families, with finite output reference grids. Several deliberately introduce adversarial branches to probe limitations of sparse evaluation; their relative frequency cannot be used as a production estimate. The actual reviewed source files do not change over their eligible adjacent first-parent Git history. Three historical business override text records exist on non-main branches but lack authentic approval signatures and decision provenance. The native functions were executed in isolation, not through an end-to-end deployed LEAP workflow; downstream displayed-state propagation uses an existing constructed trace. No independent human or organizational authority outcomes have been adjudicated, and the web research frontier check is bounded to the stated sources and access levels. These boundaries prevent an operational-validity or cross-organization improvement claim.
