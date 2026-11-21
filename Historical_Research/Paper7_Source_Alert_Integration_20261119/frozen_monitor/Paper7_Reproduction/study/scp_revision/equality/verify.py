"""Replay the version-equality signature using alternating canonical tokens."""
from pathlib import Path
import json
import sys

root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root / "implementation"))
from monitor import monitor

def canonicalize(trace):
    current = {"c": 0, "p": 0}
    previous = None
    for event in trace:
        recoded = dict(event)
        for field in current:
            if previous is not None and previous[field] != event[field]:
                current[field] ^= 1
            recoded[field] = str(current[field])
        for kind in ("o", "s"):
            if kind in event:
                packet = dict(event[kind])
                for field in current:
                    packet[field] = recoded[field] if packet[field] == event[field] else "different"
                recoded[kind] = packet
        yield recoded
        previous = event

def rows(name):
    with (root / "benchmark" / name).open() as stream:
        yield from map(json.loads, stream)

if __name__ == "__main__":
    policy = json.loads((root / "benchmark/policy.json").read_text())
    counts = {"traces": 0, "events": 0, "mismatched_sequences": 0}
    for trace, gold in zip(rows("traces.jsonl"), rows("reference.jsonl"), strict=True):
        assert trace["id"] == gold["id"]
        actual = monitor(canonicalize(trace["trace"]), policy, trace["severity"])
        counts["traces"] += 1
        counts["events"] += len(actual)
        counts["mismatched_sequences"] += actual != gold["outputs"]
    print(json.dumps(counts))
    sys.exit(bool(counts["mismatched_sequences"]))
