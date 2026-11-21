"""Independent reviewer checks; does not rerun frozen experiments.
Run with: python3 -B integration/review_checks/check_representations.py
"""
import csv
import itertools
import json
from pathlib import Path
import runpy

BASE = Path(__file__).resolve().parents[1]
CODE = runpy.run_path(str(BASE / "run_integration.py"))
monitor = CODE["mon"].monitor
oracle = CODE["oracle"].oracle
policy = CODE["POLICY"]
records = []
for dc, dp, oc, op, sc, sp in itertools.product([False, True], repeat=6):
    context = "c1" if dc else "c0"
    policy_id = "p1" if dp else "p0"
    trace = [dict(t=t, unit="s", c="c0", p="p0",
                  o=dict(value=True, at=t, c="c0", p="p0")) for t in [0, 2]]
    trace.append(dict(t=3, unit="s", c=context, p=policy_id,
                      o=dict(value=True, at=3, c=context if oc else "oldc", p=policy_id if op else "oldp"),
                      s=dict(until=8, c=context if sc else "oldc", p=policy_id if sp else "oldp")))
    expected = oracle(trace, policy)
    assert monitor(trace, policy) == expected
    for count in [3, 5, 6]:
        packets = CODE["encode"](trace, count)
        actual = monitor(CODE["decode"](packets, count), policy)
        decisions_equal = all(all(a[k] == e[k] for k in ["state", "active", "severity"])
                              for a, e in zip(actual, expected, strict=True))
        assert decisions_equal
        if count != 3:
            assert actual == expected
        records.append(dict(comparisons=count, context_changed=dc, policy_changed=dp,
                            observation_context_matches=oc, observation_policy_matches=op,
                            suppression_context_matches=sc, suppression_policy_matches=sp,
                            decision_agreement=decisions_equal, complete_agreement=actual == expected))

with (BASE / "outputs/decision_events.csv").open() as handle:
    events = list(csv.DictReader(handle))
field_differences = {}
for strategy in ["A_file", "B_calculation", "C_documentation", "D_dual"]:
    subset = [row for row in events if row["strategy"] == strategy]
    field_differences[strategy] = {
        key: dict(numerator=sum(row[key] != row["reference_" + key] for row in subset), denominator=len(subset))
        for key in ["state", "active", "severity", "reason"]}
result = dict(scope="Independent representation review checks; no added real source cases or frozen benchmark traces",
              combinations=64, encoded_replays=len(records),
              decision_agreements=sum(row["decision_agreement"] for row in records),
              complete_agreements_by_comparisons={str(n):sum(row["complete_agreement"] for row in records if row["comparisons"]==n) for n in [3,5,6]},
              independent_event_field_differences=field_differences, records=records)
output = Path(__file__).resolve().parent / "representation_check_results.json"
output.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k:v for k,v in result.items() if k != "records"}, indent=2))
