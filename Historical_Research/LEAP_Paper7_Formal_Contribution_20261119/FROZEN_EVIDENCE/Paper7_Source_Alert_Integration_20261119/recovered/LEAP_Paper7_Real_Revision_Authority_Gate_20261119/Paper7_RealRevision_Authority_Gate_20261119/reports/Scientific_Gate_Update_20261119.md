# Paper 7 — Source-revision authority research gate

**19 November 2026 · Target journal: Science of Computer Programming · Decision: RESEARCH GATE PARTIALLY CLOSED — AUTHORIZATION EVIDENCE REQUIRED**

## 1. Scientific decision

The next scientific step is to determine whether an authentic business-approved deferral remains authorized after a documented source revision. The original Paper 7 monitoring contract and five-comparison theorem define how such a decision can be represented downstream. The missing scientific reference is the authority judgment itself. No legitimate approval status can be inferred merely from a source diff or successful code merge.

A wider read-only audit of the supplied LEAP Git archive identified **nine historical KPI source-file modification pairs across four distinct non-main-branch commit transitions**. These are genuine recorded edits, recovered with complete before/after bytes and SHA-256 identities. Six pairs preserve the executable representation according to a declared narrow comparison; three change executable source. **No pair is linked to a signed business approval or two independent reviewer judgments.**

## 2. Research design and evidence authority

The archive comprises 156 commits across all archived Git refs. The expanded scan traversed 83 parent edges and found 223 source-code file-status events (134 additions, 73 modifications, 16 deletions) in the tracked source extensions scanned. Nine **modification** events involved KPI examples in `sample_project` or `sample_project_50`. The original 27 first-parent main-branch pairs remain unchanged as reported previously: the seven initially selected KPI examples did not undergo eligible changes on main. The nine newly found pairs occur in *non-main* history.

The real-source technical comparison uses Python abstract syntax tree identity for the Python examples and a limited non-comment-token normalization for SQL/TSQL/ABAP fixtures. It is a reproducible **syntactic or code-representation test**, not an independent semantic proof and not a human approval decision. Exact raw file hashes differ in all nine.

| Pair | Actual archived source revision | Technical observation |
|---|---|---|
| P7R01 | `abap_kpi.abap` | Formula-related comments changed; non-comment tokens unchanged |
| P7R02 | `python_kpi.py` | Formula documentation added; Python AST unchanged |
| P7R03 | `sql_kpi.sql` | Energy-intensity query replaced by on-spec-rate query |
| P7R04 | `tsql_kpi.tsql` | Formula comments revised; non-comment tokens unchanged |
| P7R05 | `sql_kpi.sql` | Formula comments added; non-comment tokens unchanged |
| P7R06 | `sql_kpi.sql` | Trailing newline changed; non-comment tokens unchanged |
| P7R07 | `tsql_kpi.tsql` | On-spec-rate calculation replaced with catalyst-cost calculation |
| P7R08 | `python_kpi.py` | Formatting revised; Python AST unchanged |
| P7R09 | `KPI100.py` | Required standalone input declarations added before the calculation |

The isolated historical `KPI100.py` fixture raises `NameError` before the added declarations; after the revision it computes `Days of Working Inventory: 7300.0` from its recorded illustrative constants. For both `python_kpi.py` revisions, executable Python ASTs are identical. The original source files, test script and hashes are supplied in the case package. These observations establish only code-level changes.

A subtle source-authority problem remains: **comments can change the declared business meaning while executable code stays identical** (P7R01). A matcher that ignores all comments may retain an authorization whose scope is tied to an explanation. The present source records establish the change, not whether a particular approval covered the old or the new statement.

## 3. Authentication audit and existing study evidence

The previously audited original LEAP main-branch approval ledgers contain zero authenticated approval entries. Three override descriptions exist in an older branch but have no recorded approver, signed status, timestamp or validity decision. The connected private GitHub repository has three verified merged source-code pull requests (#5–#7), and their review-submission lists are empty. A code merge is distinct from an approved business deferral. Accordingly, none of these items supplies the required authorization reference.

I reran the already-preserved portable source-revision pilot from a separate copy. It passed its pre-fixed protocol check, its 10 selected native-override cases (six implementation/specification discrepancies), 24 constructed source comparisons, and its frozen-monitor propagation. Those 24 cases remain **controlled synthetic comparisons**; their recorded technical trade-offs are separate from the nine actual archived source edits and from the still-absent human labels.

## 4. Current publication-level research frontier

Hu, Wang, Rubin and Pradel's *An Empirical Study of Suppressed Static Analysis Warnings* (FSE 2025; DOI `10.1145/3715729`) established the prevalence and evolution of suppressions and showed that some may unintentionally hide later warnings. Li and Yang's *Tracking the Evolution of Static Code Warnings* (IEEE TSE 2024; DOI `10.1109/TSE.2024.3358283`) developed manually labeled warning-evolution cases and evaluated warning identity across code revisions. These works establish nearby operational and measurement foundations. The Paper 7 opportunity is narrower: **authority-scoped carry-forward for a previously authenticated review decision across a relevant evidence change**. The present evidence does not yet establish its answer.

## 5. Exact next step — authentic independent adjudication

The attached `CODEX_READONLY_COLLECTION_TASK.md` requests a read-only search of current Codex worktrees and authorized workflow stores for **genuine** approval/deferral records missing from the supplied archive. Codex may extract and organize primary evidence but must not invent authority or act as a human approver. The deliverable would pair original approved deferrals, source/finding revisions, status changes, expiry, authorized scope and policy with traceable primary records.

The accompanying `protocol/Prospective_Authorization_Adjudication.md` defines a blinded human adjudication with two **different qualified domain reviewers**, independent initial KEEP/REVOKE/UNKNOWN decisions, recorded rationales and disagreement resolution. No outcome has been filled in. The gate-check script correctly returns `BLOCKED` with zero authentic approvals and zero dual-adjudicated cases; it therefore calculates **no invalid accuracy statistic**.

After authentic cases are obtained, compare strict file hashing, code-fingerprint matching, identity-only carry-forward and bounded behavioral probes on the same adjudicated units. Report false-retained and false-revoked authorizations, separate unknowns, and cluster by source/approval. Only then propagate their decisions to the existing frozen Paper 7 monitor and reconstruct the paper's central thesis.

## 6. Gate matrix

| Gate | Finding | Decision |
|---|---|---|
| Archived source revisions recovered | 9 paired edits with original files and hashes | PASS |
| Technical source comparison | 6 unchanged / 3 changed under declared checks | PASS |
| Standalone Python example execution | Recorded before/after behavior reproduced | PASS |
| Existing controlled study replay | Previously frozen 24-case pilot replayed successfully | PASS |
| Authenticated original authorizations | None linked in inspected records | **FAIL** |
| Independent human authority adjudication | No qualified reviewer responses | **FAIL** |
| Authorization validity of candidate matchers | No externally adjudicated reference denominator | **NOT VERIFIED** |
| Consequential SCP contribution and manuscript | Authorization question unresolved; rejected manuscript preserved | **NOT READY** |

## Limitations

All nine new source pairs are archived branch edits from one repository and are not a representative operational sample. The SQL/TSQL/ABAP comparison is a narrow source-token check; matching tokens does not prove equivalence of all production side effects. The standalone Python execution concerns examples and declared illustrative constants. A business authority may legitimately treat comments, evidence provenance or policy changes as material even when executable tokens are unchanged. The three GitHub merges document source development, not suppression authority. Without authentic approval and independently adjudicated decisions, operational carry-forward accuracy and downstream benefit remain unmeasured.

**Release decision: paper remains on scientific hold.** The new historical-source evidence and prospective adjudication kit are complete. Codex evidence extraction and genuine human reference decisions remain required to close the empirical research question.
