# LEAP Paper 7 — Independent Strict Review Response and Release Record

**Date:** 19 November 2026  
**Manuscript:** *Version Comparisons Preserve Governance Alert Decisions Across Evidence and Policy Revisions*  
**Target:** *Science of Computer Programming* (Elsevier), research paper  
**Review material:** Independent Peer Review, supplied 19 November 2026 (`Pasted text(20261119-074837).txt`)  
**Decision:** **Targeted scientific and production revision completed; journal/author administrative verification remains recorded separately.**

## 1. Scientific result retained

Paper 7 investigates which version relationships must be available to a temporal review monitor to preserve its displayed state, active episode, severity, and reason. The revision retains the frozen evaluation: **4,935 constructed traces and 26,430 events**, including **987 held-out base traces (5,286 events)**. In the no-suppression-binding ablation, **987/987 active-episode sequences** are unchanged while **30 of 987 complete decision sequences** change, comprising **48 event decision tuples**. Both Tables 4 and 5 retain their original data verbatim.

## 2. Finding-by-finding closure

| Review finding | Resolution | Evidence and location | Decision |
|:--|:--|:--|:--|
| **M1 — Six-comparison redundancy** | Added **Proposition 4**, establishing that five Boolean comparisons suffice for decision and reason under the specified reason-selection priority. The original six-comparison sufficiency proposition and three-comparison decision-only proposition are retained, with numbered references updated. Abstract, contribution, Discussion, and Conclusion now report three versus five. | *Information requirements*, new Proposition 4 and proof. Post-review `five_comparison_check.py` canonicalized original input versions and matched **4,935/4,935 complete output traces and 26,430/26,430 event outputs**, including reason. | **CLOSED** |
| **M2 — Reset variable reused** | The categorical reset reason is **R_i**; the Boolean joint version change is **Delta_i**. Equation (1) and the decision-only proposition use distinct symbols. | *Concurrent conditions and the reported reason*; *An interface for decisions alone*. PDF equation/notation inspected. | **CLOSED** |
| **M3 — Rule-family severity missing** | Table 1 now includes the **exact archived categorical severities** for all five recovered predicate families, with explicit provenance in the caption and text. | `analysis/design_inventory.csv` in the unchanged reproduction archive: privacy=`CRITICAL_PRIVACY_ALERT`; execution=`SECURITY_VULNERABILITY`; audit=`COMPLIANCE_AUDIT_GAP`; transfer=`REGULATORY_RISK`; lineage=`AUDIT_INCOMPLETE`. | **CLOSED** |
| **M4 — Missing 2025 successor** | Added **Guan and Legunsen (ICSE 2025)** and its distinct contribution: instrumentation reuse across changing programs and monitoring overhead/new-violation preservation, versus Paper 7's evidence/policy applicability and reason output. Expanded the individual-work comparison matrix. | *Versioned evidence and notification suppression* and Table 2; DOI **10.1109/ICSE55347.2025.00099**. Full text inspected from the authors' Cornell PDF; 2,028 revisions, 66 projects, 160 specifications. | **CLOSED** |
| **M5 — Execution not supplied to reviewer** | Recovered and included the original frozen reproduction archive. Package checksum verification, documented offline replay, retained replay, independent raw-output rescore, intervention taxonomy audit, and concurrent-condition checks passed. Added a distinct five-comparison representation check. | Original `LEAP_Paper7_Reproduction_20261118.zip`, unchanged SHA-256; logs in `verification/`; original **270/270 metrics** recovered, **825/825 intervention records** and **96/96 concurrent implementation-case checks** passed. | **CLOSED** |
| **M6 — Process information in captions** | Removed ChatGPT/Codex/Matplotlib preparation history from Figures 1–2 captions and condensed duplicate figure-production prose. Retained reproducibility details with the research-materials statement and preserved the approved AI declaration. Figure artwork and quantitative values are unchanged. | Figures 1–2 captions, Methods, Research materials and original figure asset checksums. | **CLOSED** |

## 3. Five-comparison proof and reproducible check

The five indicators at event *i* are `(Delta_context, Delta_policy, Observation_context_match, Observation_policy_match, Suppression_joint_match)`.

The two change indicators select the policy/context reset and its ordered reason. The two observation indicators select the first applicable mismatch reason, after which the retained time, Boolean value and packet-presence information determine other validity checks and state transitions. Suppression changes the displayed state only when an episode is active, expiry has not occurred, and **both suppression version fields match**. The reason-selection rule emits `SUPPRESSION` when the suppression actually affects the display; it never emits a distinct reason for a suppression-context mismatch versus a suppression-policy mismatch. Their conjunction therefore replaces the two separate suppression comparisons.

The additional post-review replay recoded every frozen trace using just those five comparisons and the retained non-version fields, and ran the original monitor on the recoded inputs. It compared the complete `(state, active, severity, reason)` outputs to the frozen reference. Results: **4,935 matching traces, 26,430 matching event outputs, zero output differences**. This check verifies a representation property under the frozen contract; it is not a new independent monitor or a proof of global minimality.

## 4. Exact reproduction performed in this revision

The original archive's documented command is:

```bash
cd Paper7_Reproduction
python -B run_all.py ../paper7-run
```

During this session the all-in-one wrapper exceeded the execution limit **after its first three commands succeeded**. The remaining exact verification components were run separately on the retained replay copy, with these results:

| Check | Outcome |
|:--|:--|
| Original package checksum check | PASS |
| `study/reproduce.py` full deterministic offline reproduction | PASS |
| `scripts/retain_replay.py` | PASS |
| `scripts/independent_audit.py` | PASS — all 270 metric rows; 4,935 traces; 26,430 events; external engine raw outputs concordant |
| `strict_revision/method/audit_taxonomy.py` | PASS — 825 of 825 records |
| `strict_revision/method/run_targeted_checks.py` | PASS — 24 cases, 96 of 96 implementation-case checks |
| Post-review `five_comparison_check.py` | PASS — all 4,935 complete traces and 26,430 event outputs, including reason |

Execution logs, independent metrics, input/source hashes, and the post-review test script are included in the complete archive. The five-comparison result is explicitly separated from the original frozen study.

## 5. Manuscript and production verification

- **PDF:** 22 pages, built with the Elsevier `elsarticle` class, correct author metadata, three unchanged original PDF figures, and five tables.
- **Formal content:** five propositions (the original four plus the new five-comparison proposition). Original Propositions 1–3 are byte-identical to the recovered Gold source. The decision-only original proposition changes only its Boolean variable name from `r_i` to `Delta_i`.
- **Results protection:** the three original quantitative/taxonomy table bodies outside amended Tables 1–2 are byte-identical; original figure PDF SHA-256 values are identical; the original reproduction ZIP is byte-identical.
- **References:** all **31** entries in the current bibliography are included in a successfully generated BibTeX bibliography. New source IDs for Hinov (2026), Legunsen et al. (2019), and Guan and Legunsen (2025) have checked publisher/primary identities. A complete new full-text review of every reused source was not performed.
- **Compilation:** `bibtex8 -8 Paper7`, followed by `pdflatex` passes. The final pass contains no unresolved references or overfull boxes. The PDF was rendered page-by-page and visually inspected, including the Table 1 severity column, Table 2 continuation, propositions, quantitative tables, and references.
- **Source alignment:** the November 19 final 22-page PDF was used as the content reference. Its matching November 19 editable LaTeX was unavailable in the recoverable files. The November 18 Gold LaTeX was therefore used as an editable baseline, restoring the identifiable November 19 editorial changes and citations before applying M1–M6. The historical 22-page PDF and original Gold LaTeX are preserved in the complete archive. The current PDF was freshly compiled from the delivered current LaTeX.

## 6. Journal release status

**Scientific revision: COMPLETE.** All six targeted findings are closed through source edits and recorded tests. This revision makes no claim about acceptance or actual journal submission.

### Limitations and outstanding administrative verification

The current live, title-specific *Science of Computer Programming* Guide for Authors could not be independently retrieved from the publisher in this run. Funding, competing-interest statements, original-work/exclusivity attestations and any required CRediT statement are author-specific facts not established by the supplied evidence. These items remain to be completed accurately at the publisher's submission interface. The manuscript's empirical scope remains the specified constructed policy, source-rule families, and shared temporal templates, as stated in its dedicated Limitations section.
