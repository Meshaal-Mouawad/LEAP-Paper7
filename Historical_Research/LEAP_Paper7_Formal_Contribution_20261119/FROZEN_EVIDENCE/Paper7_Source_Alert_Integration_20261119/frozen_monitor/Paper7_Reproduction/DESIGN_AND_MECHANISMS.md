# Paper 7 design and mechanism data

The saved temporal benchmark contains five families (privacy, dynamic execution, audit, transfer and lineage), 329 base designs per family, and three variants per design. The private lexical snapshots were removed before this reproduction. `analysis/design_inventory.csv` preserves each trace's source label, family, rule, severity, partition, mechanism, variant, event count and reference-state counts. `study/benchmark/traces.jsonl` contains the full temporal events. Policy durations are D=2 s, C=2 s, E=4 s and F=2 s, with inclusive dwell/clear/escalation/freshness thresholds and exclusive suppression expiry.

| Design group | Base designs per family | Saved mechanism labels | Explicit behavior exercised |
|---|---:|---|---|
| Exhaustive short sequences | 256 | `exhaustive` | Length-four combinations over the four observation symbols; persistence, pending, clearing and unresolved evidence. |
| Long controls | 3 | `control` | Stable normal/alert behavior and activation followed by clearing across longer sequences. |
| Observation quality interventions | 20 | `missing`, `conflict`, `stale`, `future` | One intervention at each of five positions for each type. |
| Evidence/version interventions | 20 | `context_old_obs`, `policy_old_obs`, `context_fresh`, `policy_fresh` | Reject obsolete evidence and reset or retain qualification according to explicit context and policy identity. |
| Suppression interventions | 15 | `suppression_valid`, `suppression_old_context`, `suppression_old_policy` | Accept current bindings and reject obsolete suppression context/policy. |
| Timing boundaries | 15 | `boundary_dwell`, `boundary_clear`, `boundary_escalate`, `boundary_freshness`, `boundary_suppression` | Below, equal and above each boundary. |
| Total | 329 | 18 labels | All related transformations remain in one partition. |

The independent audit checks 1,645 groups with exactly one `base`, one `metadata` and one `milliseconds` trace each. Development and held-out sets have disjoint family and simulated-source labels. Base and transformed variants share temporal design templates. `analysis/base_mechanism_metrics.csv` reports each family/mechanism/method without tripling the denominator through transformations. `analysis/endpoint_metrics.csv` reproduces every original metric stratum. `analysis/denominators.csv` supplies independently calculated reference denominators.

Trace agreement requires equality of every `(state, active, severity)` tuple in the finite trace. Exact episode agreement requires equality of half-open contiguous active event-index intervals; a still-active final episode ends at `len(trace)`. Missed and unwarranted active counts use the reference active and inactive event denominators respectively. UNKNOWN is a displayed state and can retain an underlying active episode, so its count is not a third category in the active/inactive partition. Reason labels are scored separately.

The six field-removal witness sets are in `study/benchmark/necessity_witnesses.json` and `witness_references.json`. They retain the full left/right traces, removed-field labels and frozen expected sequences. `saved_run/results/information_classes.json` and `information_bound.json` contain the fresh projection-class calculations. The all-field equality representation and reduced decision representation are replayed by the saved third and fourth command logs. The latter preserves decisions and changes 585 reason labels: 510 policy-mismatch labels and 75 policy-change labels.

The public upstream suppression projection lives in `study/scp_revision/external_fixture/`; its protocol, original source, license, explicit mapping and freeze are supplied together. The PyContract policy, pinned upstream engine, 21 hand traces, 28 malformed cases and engine-dispatch dependency checks are under `study/r3/baseline/` and their fresh outputs under the matching `saved_run/` paths. The SQLite implementation and retrospective protocol amendment are under `study/replication_r2/`.
