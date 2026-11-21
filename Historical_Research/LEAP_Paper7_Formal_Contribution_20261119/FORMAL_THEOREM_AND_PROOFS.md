# Theorem, proofs and counterexamples

All quantifiers and domains refer to `FORMAL_DEFINITIONS.md`. Statements marked **proved** are mathematical consequences of the stated contract. Archived cases are evidence that particular source-patterns occur; constructed histories are witnesses, not measured operational histories.

## T1. Exact preservation and factorization (proved; established result)

For any deterministic required-output map `F_q:H_q→Y`, any projection `π:H_q→Z`, and fixed policy `q`, the following are equivalent:

1. `∀h,h'∈H_q, π(h)=π(h') ⇒ F_q(h)=F_q(h')`;
2. `ker π ⊆ ker F_q`;
3. there exists a deterministic `g:π(H_q)→Y` with `F_q=g∘π`.

For a declared policy class, replace `ker F_q` by the intersection over policies on comparable retained side-input fibres. For a causal online decoder, apply the same criterion at **every projected prefix**: equal projected prefixes must imply equal output prefixes, with the projected prefix determined from that history prefix. This is stronger than checking only terminal outputs.

**Proof.** (1) and (2) rewrite the definitions of the kernels. If (1), set `g(z)=F_q(h)` for any `h` with `π(h)=z`; (1) makes the choice independent of representative. Then `F_q=g∘π`. If (3), equal projected inputs have equal `g` outputs, yielding (1). The same construction on each prefix proves the causal statement provided the prefix projections are consistent under truncation. Necessity follows by applying any causal decoder to equal projected prefixes. For a class, one decoder that receives the retained policy identity can select the corresponding `g_q`; all policies must satisfy their own kernel inclusion. ∎

This is the standard output factorization/equivalence criterion, not a new source-to-decision theorem. Antignac, Sands and Schneider (2017, Section 4, Proposition 2 and Section 4.1, Proposition 3) explicitly order input preprocessors by output kernels and characterize best output-preserving minimisers. Henzinger, Mazzocchi and Saraç (2022, Sections 2.2–2.3, Proposition 6) model indistinguishable monitor prefixes and the output precision they permit. The existing manuscript's Proposition 1 is the elementary negative direction.

## T2. Coarsest output partition (proved; established result)

For a fixed output map `F_q` on histories sharing retained side inputs, `ker F_q` is the unique coarsest correct partition. For a class `P`, the coarsest correct partition is `⋂_{q∈P} ker F_q` on comparable histories, equivalently the kernel of the vector of required outputs for the class. Any correct projection's kernel must be contained in it. A representative encoding for each class attains it as a mathematical construction; no computability or finite-state implementation follows from this existence statement.

**Proof.** `F_q` itself labels each class of `ker F_q`, so that partition is correct. T1 requires every correct projection kernel to be a subset. The class case follows by requiring that inclusion for every `q` and intersecting. ∎

In particular, the frozen-policy sequence partitions are `h≈_dec h′` iff every event decision tuple agrees, and `h≈_full h′` iff both the decision and reason sequences agree. Thus `≈_full = ≈_dec ∩ ker(reason-sequence)`; the final-event partitions replace every sequence by its last tuple. The policy-class partitions intersect the corresponding relations across all policies in the class. These exact descriptions do not by themselves provide a computable encoder.

The smallest fixed-length code for a finite fibre with `k` output classes needs at least `ceil(log2 k)` bits and an enumerated class label of that length is sufficient. The lower bound is the pigeonhole principle. The phrase *minimal information* is justified only after the fibre, output and policy class are fixed.

## T3. Source reset under the declared OR contract (proved for a restricted interface)

Restrict to a single `s_before→s_after` transition and histories whose source-dependent operation is exactly the frozen monitor's reset test `u=δ_C∨δ_D`. Retain all non-source event data, policy identities and packet match relations. On this restricted source-reset interface, `u` is sufficient. If the admissible histories include a positive episode active before the transition and a fresh positive observation at it, **one bit is necessary and sufficient** to encode whether a source reset occurs. Separate `δ_C,δ_D` bits are not necessary for `O_dec` or `O_full` on this contract.

**Proof of sufficiency.** For any two histories with equal `u` and equal retained inputs, the context-reset Boolean agrees. By the monitor transition definition, every subsequent state update and output agrees inductively if subsequent change and packet-match signals also agree. This is precisely the source-dependent information used by the contract. **Lower bound.** Take fresh positive samples at `t=0,2,3`, with `D=2`. At `t=2` the episode is active. At `t=3`, `u=0` leaves it active and displays `ACTIVE`, while `u=1` resets and yields `PENDING` with activity false. A constant zero-bit source projection equates these two admissible histories but their `O_dec` differs. Therefore at least two source classes, hence one bit, are required; `u` supplies that bit. ∎

This theorem does **not** say that one bit supplies a persistent identity for arbitrary observation or deferral packets. Their match-to-current relationships remain side inputs in the theorem. If these are removed, equal `u` can pair a matching observation with an obsolete one, giving `ACTIVE` versus `UNKNOWN` after qualification. Source signatures do not themselves establish that revalidation on a documentation change is needed.

## T4. When separate source indicators are required (proved for the declared comparison class)

For `P_sep`, assume all four source patterns `00,01,10,11` are admissible, and the output vector records the decision of both the C-sensitive and D-sensitive reset policies under the same active-before-transition witness. Then four distinct output-vector classes occur, so **at least two bits** are necessary; `(δ_C,δ_D)` is a matching sufficient two-bit code for the source reset choice.

**Proof.** In the witness of T3, the C-sensitive policy returns `PENDING` exactly when `δ_C=1`; the D-sensitive policy returns `PENDING` exactly when `δ_D=1`. Thus the vector distinguishes all four patterns. A code with fewer than two bits has fewer than four labels and merges two distinct vectors. The pair of indicators determines each reset test and is sufficient for the source decision under the retained side-input contract. ∎

All four patterns occur in the archive: `P7R06=00`, `P7R01=01`, `P7R09=10`, `P7R03=11`. `P_sep` is a comparison class, not the selected frozen revalidation policy. For arbitrary policies that inspect raw source or arbitrarily long histories with packet bindings, no universal fixed bit count follows from these four patterns. Over unbounded event sequences, the number of possible output sequences itself is unbounded; a constant-length code for the entire sequence cannot preserve them all.

## P2. Restricted-strategy witnesses (proved conditional on opaque identity interface)

Here `π_b` reveals the binding's equality pattern over a transition and retains the side inputs specified in `FORMAL_DEFINITIONS.md`; it supplies no raw source or digest-to-source lookup. The reference question is the selected dual `u` contract. A common constructed history uses fresh positive observations at `t=0,2,3,5`, changes source at `t=3`, and uses `D=C=F=2`, `E=4`. At `t=2` the episode is active. If dual detects change, at `t=3` it resets to `PENDING/false/NONE/CONTEXT_CHANGE`; otherwise it remains `ACTIVE/true/High/STATE`.

| Restricted strategy | Archived source pairs with equal strategy change signal | Signal | Different dual requirement | Consequence |
|---|---|---:|---|---|
| Whole-file `b_H` | P7R01 (D-only), P7R06 (neither) | 1,1 | 1,0 | False reset cannot be distinguished from required reset by file-change bit alone. |
| Calculation `b_C` | P7R01 (D-only), P7R06 (neither) | 0,0 | 1,0 | D-only reset is missed. |
| Documentation `b_D` | P7R09 (C-only), P7R06 (neither) | 0,0 | 1,0 | C-only reset is missed. |

The constructed histories have equal retained times, policy, observation values, initial state and strategy equality pattern, but distinct dual-reference `O_dec` at `t=3`. T1 forbids a decoder from the restricted signal that is correct on both. `COUNTEREXAMPLES_AND_CHECKS/results.json` records the frozen-monitor outputs. The archived IDs establish **source patterns**, while the event times and observations are **constructed**. A richer projection retaining raw file hashes plus a complete external lookup can distinguish these cases; these witnesses do not refute that different interface.

## P4–P5. Temporal and diagnostic reconciliation (proved for the frozen transition structure)

The existing six-, five- and three-comparison propositions are **sufficiency** results. Their proofs induct on the entire event prefix with equal initial state and retained non-version data. For `O_full`, the five signals retain separate context/policy reset and observation mismatch causes, while a deferral's two match flags can be joined because an inapplicable deferral gets no separate mismatch reason. For `O_dec`, joint reset, observation match and deferral match suffice because reset cause and mismatch cause have the same decision transition. Each event advances identical timers/activity; therefore the induction covers arbitrary finite valid histories, not one event only. Source pair bits alone are a different projection and cannot replace these temporal comparisons.

The three-comparison interface is not generally sufficient for `O_full`: two first events with equal retained data and a positive observation have, respectively, a context mismatch and a policy mismatch; both encode `observation applies=false`, both return `UNKNOWN/false/UNKNOWN`, but reasons differ (`CONTEXT_MISMATCH` and `POLICY_MISMATCH`). This valid distinguishing pair proves a lower bound of **two reason classes** within that fibre. It does not prove five signals are globally minimal. Similarly, a context-only and policy-only current change may preserve `O_dec` but differ in reset reason. The archived integration's 180/1512 reason discrepancies for the three-comparison decoder are finite checks, not a necessity proof.

**Complete temporal induction.** Let the inductive state before event `i` be `(active,positive_start,negative_start,opened_at,prior_identity,last_time)`. At the empty prefix both histories use the same specified initial state. Assume their states and retained inputs agree before event `i`. The retained reset signal determines whether activity and all three timers clear; for `O_full` the separate current-change flags also select `POLICY_CHANGE` over `CONTEXT_CHANGE` when both change. The retained observation presence, match flags, normalized times, value and `F` choose the same first applicable fault in the fixed missing→context→policy→future→stale→conflict order. A fault clears qualification and clearing starts, displays `UNKNOWN`, and retains post-reset activity. In the valid branch, equal value/time and equal prior timers make the positive or negative run and its threshold comparison identical, including equality at `D` or `C`; `opened_at` and escalation at `E` also agree. The retained joint deferral match, presence, expiry and current time select the same suppression overlay, with `t=until` inapplicable. The resulting decision tuple and successor state are identical. For `O_full`, the separate reset and observation-match flags select the same reason; joining only the deferral matches loses no reason distinction. This closes the induction for every finite prefix and hence the complete sequences. The three-comparison case follows by omitting only distinctions used to choose a reason. The 14 targeted temporal checks in `results.json` exercise these branches against the frozen monitor. They corroborate the implementation; enumeration does not replace this proof.

## P6. Contribution challenge and counterexamples to overclaims

- `δ_C∨δ_D` is sufficient for the **selected reset requirement**; the requirement is an input to the theorem, not established by it. The archived 10/20/5 complete-sequence disagreements measure alternative bindings against that selected rule; they do not validate it independently.
- Two separate source bits are **not** universally minimal. T3 gives a one-bit counterexample under the actual OR reset contract. Antignac et al. explicitly use OR to show joint minimisation can collapse three of four input cases (Section 4.2).
- Raw-source semantic preservation does not follow from `C,D`: the signatures are structural/generated proxies. A policy that directly reads bytes can distinguish two snapshots with equal `C,D`, so a theorem over every possible source-sensitive policy is false.
- A terminal-event theorem is weaker than a sequence theorem. For example, the T3 no-reset and reset histories can converge to an identical `ESCALATED` final display after enough fresh positives, while their earlier decisions differ.

**Scientific assessment:** T1–T4 and the witnesses are correct bounded results. T1/T2 are established monitor abstraction and data-minimisation facts. T3/T4 are direct specializations of those facts and the declared OR/reset policies, with the OR information phenomenon explicitly anticipated by Antignac et al. The record supports a useful contract-specific analysis, but no distinct consequential general formal theorem passed the closest-work challenge.
