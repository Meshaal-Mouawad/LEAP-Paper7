# LEAP Paper 7 — Focused Formal Contribution and Publication-Gap Closure

**Fixed review identifier:** **Independent Reviewer — Elliot Mercer**.

Use this exact identifier on the separate scientific review and verification reports. It is a project review identifier. Do not substitute a blank name, initials, numbers, other names, or an unnamed reviewer role. Do not attribute research authorship or external endorsement to this identifier. The manuscript retains its existing author and declarations. Keep review identifiers, review comments, review history, task instructions, and execution diaries outside the manuscript.

## 1. Task and decision authority

Complete the one outstanding scientific requirement for LEAP Paper 7: determine whether the existing evidence supports a consequential, sufficiently distinct **general formal result** connecting source-derived version information to version-sensitive governance-alert decisions. Provide a complete proof and direct comparison to the strongest published predecessors if such a result exists. Integrate it into the current manuscript **only after** its scientific validity and significance pass verification.

Retain the research owner's authority over manuscript content and scientific decisions. Execute the task without routine permission requests. Do not submit, publish, push, merge, overwrite an authoritative source, alter an archival record, or change the existing experiment. Create a separate working version and deliver the complete new results in a ZIP.

**Journal:** *Science of Computer Programming*, research article.

**Primary inputs (located in the attached package):**

1. `INPUTS/01_CURRENT_MANUSCRIPT.pdf` — authoritative corrected 30-page manuscript.
2. `INPUTS/02_CURRENT_LATEX_SOURCE.zip` — matching editable source, references, and figures.
3. `INPUTS/03_FROZEN_SOURCE_TO_ALERT_EVIDENCE.zip` — nine original source-revision pairs, source-to-alert integration, 63 constructed contexts, 252 comparison streams, preserved monitor and historical benchmark.
4. `INPUTS/04_LAST_EDITORIAL_ASSESSMENT.pdf` and `INPUTS/05_EDITORIAL_DECISION.md` — latest decision and exact outstanding scientific issue.
5. `INPUTS/06_CLOSEST_WORK_LEDGER.csv` — previously checked publications and access records.
6. `INPUTS/07_GOLD_NICHE_PROTOCOL.md`, `INPUTS/08_RESEARCH_GAP_METHOD.md`, and `INPUTS/09_WRITING_PROTOCOL.md` — governing research, novelty, and writing standards.
7. `CURRENT_VERIFIED_FACTS.md`, `SOURCE_INDEX.md`, and `CHECKSUMS_SHA256.csv` — factual baseline, file locations and input checksums.

## 2. Fixed research baseline — do not repeat or modify

- Nine archived source-revision pairs across four Git transitions. Representations: calculation and generated KPI documentation. Reported categories: two both changed; one calculation representation only; four documentation only; two neither.
- Seven **constructed** monitoring contexts per source pair, producing 63 pair–context units, four strategies and 252 strategy streams (1,512 event outputs).
- The strategy-specific decision-sequence disagreements against the declared dual-output reference are 10/63 for whole-file, 20/63 for calculation-only, 5/63 for documentation-only, and 0/63 for dual-output. Zero for the reference is expected by construction and is a conformance result.
- All 252 strategy streams and 1,512 event outputs match the preserved monitor reference under their respective inputs.
- Three joint comparisons preserve displayed state, activity and severity for the specified lifecycle policy. Five and six comparisons also preserve the recorded reason field. Three comparisons do not preserve all reason labels.
- The historical 4,935-trace lifecycle study, 987/987 episode agreement and 957/987 complete-decision agreement concern a different existing analysis. Keep its denominators separate.
- The calculation representation is a structural signature, not a universal proof of unchanged program output. No real operational alert histories accompany the nine revisions.
- The last editorial assessment found **one unresolved scientific issue**: the decision to revalidate on change in either representation was selected as the reference objective. Its validity as a broader scientific or operational requirement has not been independently established.

No new case counts, source revisions, approval records, quantitative improvements, or tests may be declared without actual reproducible evidence. Do not interpret the 63 constructed contexts as independent source revisions.

## 3. Precise research question

**Under what necessary and sufficient conditions does a source-revision information projection preserve the outputs required by a version-sensitive monitoring policy, and when can a coarser projection demonstrably fail?**

Answer separately for:

- the decision tuple: displayed state, episode activity and severity;
- the diagnostic reason label;
- the source representation: executable-structure signature and generated-documentation signature;
- the complete temporal history, retained monitor state and policy identity.

This is an output-relative theoretical question. Do not presume that keeping two separate change bits is universally minimal. When the policy only asks whether either representation changed, a single combined change indicator can be sufficient. Establish the exact conditions under which separate indicators contain information that the required output can distinguish.

## 4. Formal model — specify every object before proving anything

Start with a fully defined mathematical model, consistent with the actual source files and the frozen monitor:

1. Define the source-revision pair `s_before, s_after` and the two reproducible extraction functions `C(s)` and `D(s)` for calculation representation and generated documentation. Define their domains, comparison operation, and the limits of what they measure.
2. Define change indicators `delta_C` and `delta_D` by equality of these extracted representations. Distinguish these from true program-semantic equivalence.
3. Define the class of admissible source-to-evidence binding functions `b`, including the fixed whole-file, calculation-only, documentation-only and dual-output strategies. Explain exactly when these functions assign equal evidence identities to two revisions.
4. Define a valid time-ordered monitoring history containing the evidence and policy identities, observations, deferrals, event times and preserved monitor state. State the existing input-validation rules and temporal semantics; do not revise them.
5. Define the deterministic monitor and two output projections: `O_dec` for displayed state/activity/severity and `O_full` for that tuple plus reason.
6. Define a reduced information projection `pi` on admissible monitoring histories. State explicitly which side inputs and initial state are retained. Two histories are indistinguishable under `pi` only when all retained information agrees.
7. Define the applicable policy class `P` and quantify carefully: a theorem for one fixed policy is different from a theorem for every policy in a declared class.
8. Define *output preservation* by the property: whenever two admissible histories have the same reduced representation, their required outputs agree. Explain whether outputs are final-event values, full event sequences, or both.

Use formal notation consistently in the manuscript. Definitions, assumptions and model restrictions belong adjacent to the mathematical statement. Do not silently elevate a contract-specific conclusion into an unrestricted theorem.

## 5. Mandatory proof obligations and counterexamples

**P1 — Correctness criterion.** Derive and prove the exact necessary-and-sufficient output-preservation condition for the declared projection and policy class. Determine whether this is already the standard equivalence/factorization result; give proper attribution if so.

**P2 — Source-channel distinguishability.** For each restricted information strategy, determine whether there exist two admissible source revisions indistinguishable to that strategy but distinguishable by the required monitor output. Supply a complete, inspectable witness or prove that no such witness exists under the stated contract. Record actual archived source-pair identifiers separately from constructed monitoring histories.

**P3 — Minimal information.** Characterize the coarsest correct information partition for each required output under the declared policy class. Explicitly test whether one combined change bit suffices, when two channel indicators are necessary, and when no fixed bit count follows. Do not use the term *minimal* unless a lower bound and matching sufficient representation have been proved.

**P4 — Decision versus reason.** Reconcile the theoretical result with the existing three-, five- and six-comparison propositions. Distinguish proven sufficiency from proven necessity. Establish any new lower bound only through a valid distinguishing-history argument.

**P5 — Temporal consistency.** Check the proof against version resets, stale and future observations, mismatched deferrals, expiry at the event boundary, concurrent faults and the specified reason-precedence order. A proof using only one static event does not establish a temporal-history theorem.

**P6 — Contribution challenge.** Identify which propositions follow immediately from standard monitor abstraction theory, and which genuinely add a nontrivial source-to-decision theorem. If the new result is a direct specialization of existing work, report that plainly rather than rebranding it as independent novelty.

Use targeted finite enumeration or a formal checker only to test candidate lemmas and generate counterexamples. Supply actual executable scripts and results where computational checks are claimed. A finite check cannot stand in for a universal mathematical proof.

## 6. Published-research comparison — exact targets

Before claiming a new theorem, compare it to the pivotal references in the included ledger and manuscript, specifically:

- Henzinger, Mazzocchi and Saraç (2022): monitor abstractions and observational indistinguishability.
- Antignac, Sands and Schneider (2017): functionality-preserving input minimisation.
- Guan and Legunsen (2025): evolution-aware monitoring.
- Jiang and colleagues (2026), FineMOP: selecting specifications for renewed monitoring after source changes.
- Gröninger and colleagues (2025), ChangeGuard: analysis of behavioral change across revisions.
- Huang, Chen, Chen and Zhou (2024), CoCC: changed source code and stale comments.
- Hu and colleagues (2025): warning suppression behavior over software evolution.
- Relevant *Science of Computer Programming* papers on monitoring, code evolution and generated documentation in 2024–2026.

For each pivotal work, record exact title, authors, year, venue, DOI/URL, access level, problem, formal assumptions, demonstrated result, and the precise distinction from the proposed proposition. Verify claims against accessible primary passages; distinguish full-text checks from abstract-only or metadata-only checks. Search for equivalent statements using different terminology. Do not declare a general result new simply because the application vocabulary differs.

Prepare one comparison table with these columns: `Predecessor | Established theorem or result | Assumptions | Present proposed theorem | Concrete additional knowledge | Evidence | Verdict`. The table must withstand the closest-predecessor challenge.

## 7. Decision gate — decide before editing the manuscript

Issue exactly one result:

**PASS — substantiated formal advance.** At least one correct, nontrivial, clearly bounded theorem survives the closest-work comparison. Its proof and reproducible witnesses are complete. Integrate that result into a separate new manuscript version, update the abstract/introduction/related work/discussion/conclusion only where logically required, compile the PDF and inspect the rendered pages.

**PARTIAL — formal result correct; significance unresolved.** Preserve the current manuscript unchanged. Deliver the exact theorem, proof, closest-work comparison and the one unresolved source or proof obligation. State the smallest action needed for a decision.

**FAIL — no supported distinctive formal advance.** Preserve the current manuscript unchanged. Record the closest existing result that subsumes the candidate, or the specific counterexample disproving it. Give an evidence-grounded recommendation for the existing bounded study rather than inventing a new experiment.

Do not manufacture a PASS. Do not make revision conditional on an arbitrary count of citations, test cases or additional pages. Do not rewrite a verified proposition unless a documented mathematical error requires correction.

## 8. If PASS: manuscript integration requirements

- Use the exact existing LaTeX source and bibliography from the package; preserve the base version separately.
- Keep the original five proposition/proof environments, numerical results, 252-stream results, reference method, original figures and citation identities unchanged. Place the new result next to the existing information-preservation analysis; number and cross-reference it correctly.
- Explain the theorem through a source-grounded example followed by definitions and proof. Show how it changes the interpretation of the recorded 10/20/5 disagreements.
- If new claims alter the title or abstract, change them only to match the theorem actually proved. No extrapolation to unrecorded operational outcomes.
- Avoid duplicate paragraphs, defensive prose, manuscript-history commentary and irrelevant new figures.
- Keep the original author, affiliations, research ownership and existing declarations unchanged. Do not insert the review identifier or any process metadata into the scientific text.
- Run a full LaTeX build, citation checks, mathematical notation check, figure/text audit and page-by-page rendered inspection. Compare protected sections with the frozen baseline and record all authorized differences.

## 9. Exact output folder and required filenames

Create only new files under `LEAP_Paper7_Formal_Contribution_20261119/`, with these deliverables:

1. `README.md` — exact source identities, run/build commands, decision and how to inspect findings.
2. `FORMAL_DEFINITIONS.md` — formal objects, domain assumptions, source signatures, projections, policies, outputs and equivalence definitions.
3. `FORMAL_THEOREM_AND_PROOFS.md` — every proposed theorem, full proof, lower bound if justified, known related theorem and full counterexamples.
4. `COUNTEREXAMPLES_AND_CHECKS/` — evidence-derived or constructed cases, executable checker, machine-readable results, and an explanation of what was actually checked.
5. `CLOSEST_WORK_COMPARISON.csv` — source-by-source literature challenge with claim-support and access level.
6. `SCIENTIFIC_CONTRIBUTION_VERDICT.md` — PASS/PARTIAL/FAIL with direct supporting evidence, exact residual work, and journal relevance.
7. `INDEPENDENT_REVIEW_Elliot_Mercer.md` — review report labeled exactly `Independent Reviewer — Elliot Mercer`; mathematical objections, precedent comparison, PASS/FAIL per proof obligation, source locations and verification commands. The designation is a fixed project label, not a personal signature.
8. `REPRODUCIBILITY_AUDIT.md` — commands actually run, exit status, matched outputs, checked checksums and tests not executed.
9. `CHANGE_LOG.md` — location, reason, evidence and effect of every substantive change.
10. `FINAL_MANUSCRIPT/` — populated with `Paper7.tex`, bibliography, figure sources and compiled `Paper7.pdf` **only for PASS**; otherwise include `UNCHANGED_BASELINE.md` identifying the preserved current manuscript.
11. `MANIFEST_SHA256.csv` — SHA-256 checksums for every final output file, excluding the manifest itself.
12. `LEAP_Paper7_Formal_Contribution_20261119.zip` — complete reproducible delivery archive.

No empty reviewer-name fields, fabricated research credentials, placeholder judgments, proposed-only deliverables presented as complete, or invented execution outcomes. Explicitly classify what was proved, what was checked computationally and what is an interpretation.

## 10. Completion checks

Before delivery, perform each applicable check and record PASS/FAIL/NOT VERIFIED:

- Input file identity and archive extraction.
- All previous empirical results and mathematical propositions preserved.
- Formal statement has clear quantifiers and model assumptions.
- All proof steps valid; counterexamples trace to declared inputs.
- Necessary/sufficient/minimal claims use correct logic.
- Decision and reason outputs evaluated separately.
- Strongest published precedents compared accurately.
- New theorem distinguishes a consequential capability, not merely an existing equivalence expressed with new labels.
- Final manuscript and rendered PDF synchronized when PASS.
- Reviewer role designation appears in review reports only.
- ZIP integrity and final-file checksums verified.

**Finish the task in the current session. Deliver the new ZIP, the contribution verdict, and the complete mathematical result. The existing 252-stream study remains frozen.**
