# Independent Reviewer — Elliot Mercer

**Scope:** separate scientific verification of the Paper 7 formal-contribution task. The identifier above is a fixed project review label, not research authorship, a personal signature or an external endorsement. Review date: 20 November 2026 (Asia/Riyadh). Baseline: `INPUTS/01_CURRENT_MANUSCRIPT.pdf` and byte-matched `BASELINE_SOURCE/Paper7.tex`.

## Direct finding

**Scientific contribution verdict: FAIL — no supported distinctive formal advance.** The main correctness and coarsest-partition claims are valid but standard factorization/kernel results. The proposed OR reset specialization is explicitly anticipated by Antignac et al.'s OR example. The separate-channel lower bound holds only for a declared comparison class with both channel-sensitive policies; it is not a property of the selected frozen OR policy. The manuscript stays unchanged.

## Proof-obligation review

| Obligation | Result | Mathematical objection or verification | Source location / check |
|---|---|---|---|
| P1 correctness criterion | PASS for validity; FAIL as novelty | T1 proves necessary and sufficient kernel inclusion and factorization. It is established output-minimisation theory. | `FORMAL_THEOREM_AND_PROOFS.md` T1; Antignac 2017 Section 4 Proposition 2; Henzinger 2022 Proposition 6. |
| P2 source-channel distinguishability | PASS with explicit interface boundary | A_file, B_calculation and C_documentation each have a pair of archived revision patterns with equal strategy change signal and differing dual-required output. Raw digest names or an external lookup would be a richer interface; this witness concerns the opaque equality-pattern interface actually used by the monitor. | `FORMAL_THEOREM_AND_PROOFS.md` P2; `COUNTEREXAMPLES_AND_CHECKS/results.json`; archived `integration/outputs/pair_categories.csv` and `change_detection.csv`. |
| P3 coarsest/minimum information | PASS with bounded quantifiers | T2 gives output-kernel partition. T3 proves one-bit lower bound plus matching OR signal on the selected source-reset contract; T4 proves two bits only for the separately sensitive class. No universal fixed bit count is asserted for full temporal histories. | T2–T4; Antignac Section 4.2 OR example; `results.json` source partition. |
| P4 decision versus reason | PASS | Existing 3/5/6 propositions establish sufficiency, not global minimality. A context-mismatched versus policy-mismatched observation gives the same decision and different reason, establishing a valid reason distinction. | `BASELINE_SOURCE/Paper7.tex` lines 271–298; `FORMAL_THEOREM_AND_PROOFS.md` P4–P5. |
| P5 temporal consistency | PASS for proof; targeted checks pass | Induction retains initial state and each event's non-version side inputs. Version reset order, concurrent fault precedence, future/stale observations, deferral mismatch and expiry boundary are addressed. Fourteen implementation branches were checked; those finite checks do not replace the proof. | Frozen `study/implementation/monitor.py` lines 18–68; `check_candidate.py`; `results.json`. |
| P6 contribution challenge | FAIL | The central general theorem and quotient are direct specializations of established output-equivalence results. Source-to-alert signatures provide a bounded case analysis; they do not prove an independently required documentation-change reset. | Antignac 2017 Section 4; Henzinger 2022 Sections 2.2–2.3; `CLOSEST_WORK_COMPARISON.csv`; `SCIENTIFIC_CONTRIBUTION_VERDICT.md`. |

## Specific counterexample to a tempting claim

Claim: *both source change indicators are necessary for every policy that reacts to either channel*. Counterexample: under the frozen reset rule, source patterns `01`, `10` and `11` all cause the same reset. The single signal `δ_C∨δ_D` separates those three from `00`. A positive episode at `t=2` yields `ACTIVE` at `t=3` for `00` and `PENDING` for each other pattern, establishing the one-bit lower bound and matching sufficiency for this restricted source-reset interface. The observation and deferral match relations remain required temporal side inputs.

## Closest-predecessor comparison

Antignac, Sands and Schneider's *Data Minimisation: a Language-Based Approach* is the strongest direct formal predecessor. Its Proposition 2 expresses the output-kernel ordering and its Section 4.2 explicitly contrasts joint minimisation of OR with separate-input minimisation. Henzinger, Mazzocchi and Saraç supply the monitor-prefix equivalence framework. iMOP and FineMOP concern changed-code monitoring effort and violation retention; ChangeGuard concerns behavioral change; CoCC concerns comment consistency; Hu et al. concern warning suppressions. Their different endpoints do not rescue a general theorem already captured by the formal predecessors. Exact titles, bibliographic identities, access levels and primary passages are in `CLOSEST_WORK_COMPARISON.csv`.

## Verification commands and observed results

From the package root:

```sh
python3 -B COUNTEREXAMPLES_AND_CHECKS/check_candidate.py
python3 -B FROZEN_EVIDENCE/Paper7_Source_Alert_Integration_20261119/verify_preservation.py
```

The first command exited 0 and reported 9 archived pair rows read, 3 distinguishing witnesses and 14 targeted temporal checks. The second exited 0 with 347/347 preserved files unchanged. The completed 252-stream experiment was not replayed. The 30-page manuscript and five existing proposition/proof environments were not edited.

## Completion gates

| Required check | Result | Direct evidence |
|---|---|---|
| Input identity and extraction | PASS | 12/12 supplied SHA-256/size rows match; nested ZIP tests passed. |
| Prior empirical and mathematical record preserved | PASS | Input archives unchanged; 347/347 evidence files and 16/16 extracted source members match. |
| Clear quantifiers and model assumptions | PASS | `FORMAL_DEFINITIONS.md` and T1–T4. |
| Proof steps and counterexamples | PASS | T1–T4 proofs; archived pair IDs separated from constructed histories. |
| Necessary/sufficient/minimal logic | PASS | One-bit and two-bit lower bounds paired with sufficient encodings only in declared classes. |
| Decision and reason separate | PASS | `O_dec`/`O_full` and reason mismatch witness. |
| Closest published precedents | PASS | 12-row primary-source comparison with access levels. |
| Consequential distinct theorem | FAIL | General kernel/OR result is subsumed; selected revalidation requirement remains an assumption. |
| Final revised PDF synchronized | NOT VERIFIED | Revision was excluded by FAIL gate; baseline PDF retained. |
| Review identifier placement | PASS | Fixed identifier is used in the generated review report and does not enter the manuscript. |
| Final ZIP integrity/checksums | PASS | See `REPRODUCIBILITY_AUDIT.md` final archive verification. |
