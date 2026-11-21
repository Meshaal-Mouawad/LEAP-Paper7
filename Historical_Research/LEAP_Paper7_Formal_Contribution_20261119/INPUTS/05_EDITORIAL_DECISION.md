# LEAP Paper 7 — Final Editorial Assessment

**Assessment date:** 19 November 2026  
**Journal:** *Science of Computer Programming* (SCP), Research Papers Track  
**Assessed baseline:** `LEAP_Paper7_Integrated_Manuscript_20261119.pdf` (30 pages)  
**Corrected version:** `LEAP_Paper7_Editorially_Corrected_20261119.pdf`  
**Decision:** **FIT AFTER SPECIFIC SCIENTIFIC WORK — NOT APPROVED FOR SUBMISSION**

## Editorial decision

Paper 7 establishes a **reproducible, bounded source-to-alert contract result**. The study identifies nine archived source revisions whose executable and generated-documentation representations change differently. Under a declared policy that requires revalidation when either representation changes, four upstream version strategies produce different downstream review decisions in 63 constructed event contexts. The existing proofs characterize the version comparisons sufficient to preserve specified decision and reason outputs.

The result is technically coherent and falls within SCP's research scope. It does **not yet establish a consequential scientific advance sufficient for a confident full research-paper recommendation**. The decisive issue is **the reference criterion**: dual-output revalidation is chosen as the study objective. Its zero disagreements are expected, and the 10/20/5 alternate-strategy disagreements establish the behavior of the chosen contract. The archive contains no independent evidence establishing when an actual documentation revision requires renewed warning evaluation. The paper neither proves an applicable result for a broader class of source-linked review contracts nor evaluates such decisions against an external reference.

**The smallest remaining scientific decision:** either (A) justify the revalidation requirement with an independently established decision criterion and evaluate it against source revisions, or (B) establish a nontrivial general formal result whose applicability does not hinge on choosing the dual-output strategy as its own reference. The existing experiment remains frozen; repeating it is unnecessary. This is a contribution-significance requirement, not a request to enlarge sample counts or recruit reviewers.

## Protected research retained

- 9 historical source-file pairs from 4 Git transitions: 2 both-representation changes, 1 calculation-representation-only, 4 generated-documentation-only, 2 neither.
- 7 constructed event scenarios per pair; 4 identity strategies; 63 pair–scenario contexts, **252 strategy streams, 1,512 event decisions**.
- Against the explicitly defined dual-output reference: 10/63 whole-file, 20/63 calculation-only, 5/63 documentation-only differing complete sequences; dual 0/63 by construction.
- 252/252 streams and 1,512/1,512 events match the unchanged policy oracle for their respective inputs. The 3-comparison encoding retains decisions; 5 and 6 retain the selected reasons.
- The historical 4,935-trace temporal benchmark and the 987/987 episode versus 957/987 complete-sequence comparison remain separate and unchanged.

## Closest-work assessment

| Scientific predecessor | What it established | Resulting boundary for Paper 7 |
|---|---|---|
| Gröninger et al., ChangeGuard, FSE 2025, DOI 10.1145/3715760 | Paired execution to detect source-code behavior changes, tested on annotated code revisions | The present executable signature is a structural measurement, not a stronger behavior detector |
| Huang et al., CoCC, *Journal of Software: Evolution and Process*, 2024, DOI 10.1002/smr.2718 | Learned detection of stale code comments using before/after information | Generated-description differences are a measured input, not a new consistency detector |
| Chen et al., *SCP*, 2026, DOI 10.1016/j.scico.2026.103524 | Empirical effects of code/AST context in description generation | Documentary generation is established; this paper traces its output-change representation into a policy |
| Hu et al., FSE 2025, DOI 10.1145/3715729 | Observed suppression evolution and unintended hiding of later warnings | Suppression hazards are established prior evidence |
| Guan and Legunsen, ICSE 2025, DOI 10.1109/ICSE55347.2025.00099 | Evolution-aware verification across 2,028 revisions and 66 projects | Earlier research already reasons about code evolution and monitor work |
| Jiang et al., FineMOP, ICSE 2026, DOI 10.1145/3744916.3787833 | Fine-grained selection of specifications for repeat monitoring across 1,104 revisions and 68 projects | The distinct endpoint here is a warning decision and reason under a source-derived evidence identity, not re-monitoring cost |
| Henzinger et al., Runtime Verification 2022, DOI 10.1007/978-3-031-17196-3_11 | Output-aware monitor abstractions and indistinguishable observation prefixes | The 3/5 comparison results instantiate existing abstraction principles for the selected policy |

This is a **targeted closest-work assessment**, not an exhaustive review of every published article. The strongest comparative sources above were checked against primary publisher records or accessible original texts. The journal's current official description verifies **subject-area fit**; its complete submission guide was inaccessible at the time of checking.

## Corrections applied directly to the manuscript

1. **Related Work and bibliography:** Corrected the author record for the 2024 CoCC study (Yuan Huang, Yinan Chen, Xiangping Chen, Xiaocong Zhou) and updated its in-text attribution.
2. **Closest predecessor:** Added the 2026 FineMOP study, its verified DOI and substantive distinction in Related Work, the comparison table, and the Discussion.
3. **Reader inspection:** Added the full **six-event P7R02/old-observation case** as a source-grounded table showing calculation-only and dual-output states, activity and reasons at 0, 2, 3, 5, 7 and 9 seconds. All table entries are extracted from the frozen `decision_events.csv`.
4. **Preservation:** The five prior proposition/proof environments, all six existing method/results tables, three figures and their source files, and raw research evidence were not modified.

## Final gate matrix

| Gate | Verdict | Evidence |
|---|---|---|
| G1: Subject fit | **PASS** | SCP official research-paper scope covers formal techniques and experimental software technology |
| G2: Consequential, distinct contribution for full research paper | **FAIL** | Two-output rule is author-selected; its decision benefit beyond contract conformance is unestablished |
| G3: First-time-reader explanation | **PASS** | LEAP, two representations, monitor contract, full worked source-to-alert sequence introduced and connected |
| G4: Question–method–finding continuity | **PASS** | Q1–Q3 answered by source pairs, 252 streams, and output-specific proofs |
| G5: Exact support of the entire bibliography | **NOT VERIFIED** | Pivotal sources verified; complete entry-by-entry claim support not redone |
| G6: Methods, units, controlled comparison | **PASS** | 9 pair units; 63 constructed contexts; 252 strategies; fixed technical reference disclosed |
| G7: Numerical results and claims | **PASS** | Fresh integration replay; raw denominators and original numerical record retained |
| G8: Scientific visuals and tables | **PASS** | Existing figures preserved; added table checked against event output and rendered PDF |
| G9: Protected-research preservation | **PASS** | Original propositions, ordinary tables, figures and 252-stream package unchanged |
| G10: Reproducibility and production | **PASS** | 347/347 preserved files pass; 13/13 regenerated integration outputs byte-identical; PDF rebuilt and visually inspected |
| G11: Scientific writing | **PASS** | Updated predecessor comparison and complete case remove two demonstrable narrative defects |
| G12: Material scientific closure | **FAIL** | Consequentiality of the chosen dual-output revalidation requirement remains unestablished |
| Venue-specific formatting | **NOT VERIFIED** | Publisher guide endpoint returned an access error; official general publisher instructions reviewed |

## Final recommendation

**Preserve the corrected 30-page manuscript and the 252-stream evidence. Do not initiate another general editorial rewrite or repeat the same experiment.** The paper is scientifically useful as an inspectable model-specific investigation. The remaining decision is whether to establish an independent revalidation criterion or elevate the argument to a general substantive theorem. Until one is supported, retain the **FIT AFTER SPECIFIC SCIENTIFIC WORK** verdict for SCP's full Research Papers Track.

## Limitations

The nine source pairs come from one archived repository; their calculation endpoint is an executable-structure signature rather than complete semantic equivalence. Alert histories are constructed and the dual-output reference is a deliberately specified revalidation policy. The existing proof obligations apply to the stated monitor and retained side inputs. No operational-effect or cross-project prevalence estimate follows. The literature check was targeted and a complete SCP submission-format inspection was not available.

## Verified public sources

- SCP official journal description: https://shop.elsevier.com/journals/science-of-computer-programming/0167-6423
- CoCC article: https://doi.org/10.1002/smr.2718
- FineMOP: https://doi.org/10.1145/3744916.3787833
- ChangeGuard: https://doi.org/10.1145/3715760
- Guan and Legunsen: https://doi.org/10.1109/ICSE55347.2025.00099
- Hu et al.: https://doi.org/10.1145/3715729
- Henzinger et al.: https://doi.org/10.1007/978-3-031-17196-3_11
- Elsevier journal policy: https://www.elsevier.com/en-gb/about/policies-and-standards/generative-ai-policies-for-journals
