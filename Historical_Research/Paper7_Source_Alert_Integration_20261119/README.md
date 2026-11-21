# Paper 7 source-to-alert integration

This addendum connects the nine archived source-revision pairs to the unchanged Paper 7 governance monitor. It preserves all earlier packages, manuscript source, mathematical material, figures, numerical results and frozen reproduction. The target journal remains Science of Computer Programming. This package is research evidence; it does not revise or submit the manuscript.

Start with `integration/outputs/RESULTS.md` and `SOURCE_RECOVERY.md`. The integration protocol is `integration/PROTOCOL.md`; all new results are computed by `integration/run_integration.py`. `INDEPENDENT_REVIEW.md` records the separate technical review.

From this directory run:

```sh
python3 -B verify_preservation.py
python3 -B integration/run_integration.py
```

The integration uses only Python's standard library, reads the preserved comparisons, and runs the frozen monitor and oracle on new explicitly constructed monitoring scenarios. It does not rerun the nine-pair source experiment or the 4,935-trace benchmark. Runtime output differences, source-representation changes, and monitoring inputs are separately identified. No historical approval or Boolean review finding is inferred from a source change.

`repository_source_verification.json` records 18/18 Git source-blob hash matches against the existing local LEAP repository. This is an additional provenance check; reproduction uses bundled snapshots and needs no Git repository. `preserved_input_manifest.json` and `verify_preservation.py` verify recovered bytes. The original reader-first manuscript and all 17 editable archive members remain preserved; `preserved_manuscript_members.json` lists their hashes.

The seven monitoring scenarios are sensitivity probes on the same nine pairs, not 63 independent real revisions. No statistical significance or measured production improvement is claimed. Complete observed temporal histories were unavailable for 9/9 pairs; conditional monitor results are reported separately.
