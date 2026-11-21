# Paper 7 offline reproduction supplement

This supplement starts at the temporal observation interface. It reproduces the primary six-method evaluation, the thirty paired witnesses and six information bounds, both representation checks, the retrospective SQLite and PyContract replays, and the four mapped Alertmanager suppression checks. It contains 4,935 constructed traces with 26,430 events, including the original 2,961 held-out traces and 15,858 held-out events. No new traces were sampled for this supplement.

## Reproduce

Use Python 3.11 or later with SQLite and `pandas` available to that interpreter. The verified run used Python 3.12.14, SQLite 3.53.1, and pandas 2.2.3. The bundled PyContract version imports pandas when it loads its CSV support. From the directory containing this README, run:

```sh
python reproduce.py
```

The runner verifies the file manifest and executes in a temporary directory without fetching packages or other files. It replays both retrospective oracles against the saved reference, checks primary, SQLite, and PyContract prediction files against their original SHA-256 digests, and reruns the information bounds, 29 reference regression cases, and four mapped upstream expectations. The equality encoding preserves the whole output. The smaller representation preserves all decision tuples and changes 585 reason labels, split into 510 policy-to-context mismatch reports and 75 policy-to-context change reports.

The PyContract replay loads the pinned upstream engine, verifies that normalization yields the same event projection as the original run, and compares all four output fields with the full incremental monitor on each identical trace. It checks one engine event and one transition per input event and reproduces the 60 witness-side, 21 hand-trace, and 28 malformed-input records. The engine-dependency test disables three dispatch methods one at a time and checks that restoring them restores the expected result. `expected/` contains the historical comparison digests and summaries. The saved references, witness inputs, study policy, and core evaluation code retain their historical bytes. The primary, SQLite, and PyContract `FREEZE` manifests for this derivative identify their historical counterparts by SHA-256. The separately frozen Alertmanager projection and its manifest retain their historical bytes.

## Data and source coverage

`benchmark/traces.jsonl` preserves the trace identifiers, partitions, family and rule labels, variants, timestamps, units, versions, freshness inputs, suppressions, metadata changes, and Boolean or unresolved findings. It omits the 18,600 illustrative observation `snapshot` strings and their 18,600 digests, fields unused by the evaluated monitors, references, and SQLite replay. The replay verifies output equivalence against both historical raw prediction files. The original archived source snapshots, repositories, drafts, knowledge-base bytes and fixture replay are outside this supplement. Re-executing the original lexical adapters or checking the eleven archived source-recovery cases requires the private research record and appropriate permissions.

Two upstream Apache-2.0 components are included with their license texts and pinned provenance. `r3/baseline/upstream/` contains the unmodified PyContract Python package, documentation, project metadata and demonstration fixture from `pyrv/pycontract` at commit `e378eed38699bcff33e2ae71426e6b161690cdfa`. The study-specific policy and runner sit outside that upstream directory. `scp_revision/external_fixture/source/` contains the unmodified `silence_test.go` from Prometheus Alertmanager v0.28.1 with its original copyright header and accompanying license. The Alertmanager projection executes the Paper 7 monitor and oracle. Four source assertions involving scheduled, overlapping, or regular-expression silences remain outside that projection and are listed in `mapping.json`. [PyContract pinned source](https://github.com/pyrv/pycontract/tree/e378eed38699bcff33e2ae71426e6b161690cdfa) · [Alertmanager pinned test](https://github.com/prometheus/alertmanager/blob/v0.28.1/silence/silence_test.go#L1372-L1443)

The supplement is prepared for author review. Public release of the Paper 7 materials and selection of any distribution license await the author's approval.
