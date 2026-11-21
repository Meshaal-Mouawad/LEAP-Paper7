# External fixture projection — verified report

Status: COMPLETE for the four-case mapped conformance check. Date: 18 November 2026.

Paper 7 reproduced all **4/4 mapped suppression expectations** from the first four `s.Mutes` assertions of Prometheus Alertmanager v0.28.1's `TestSilencer`. The mapping covers **4/8 assertions** in that upstream test. The other **4/8** remain explicitly outside the native policy and are preserved in `mapping.json`.

| Source assertion | Line | Source expected `Mutes` | Paper 7 suppressed | Final Paper 7 state | Active |
|---|---:|---|---|---|---|
| Absent silence | 1383 | false | false | ACTIVE | true |
| Nonmatching equality | 1392 | false | false | ACTIVE | true |
| Matching equality | 1402 | true | true | SUPPRESSED | true |
| Expired equality silence | 1408 | false | false | ESCALATED | true |

All four complete Paper 7 outputs agreed with oracle v2. All activation setup checks passed; execution failures: 0. Full decisions are in `results.json`.

## Frozen reference and provenance

- Upstream test: https://github.com/prometheus/alertmanager/blob/v0.28.1/silence/silence_test.go#L1372-L1443
- Git blob: `a65b1f6337723d3ba76140081b757088213f7d5a`.
- Source SHA-256: `5ed81fb8edec3139f31e537a397663fba2a54ce4ed0784a11035e364b9c45e96`.
- License: Apache License 2.0, full text preserved in `source/LICENSE`.
- License blob: `261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64`; SHA-256: `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4`.
- Authenticated connector retrieval recorded in `source/retrieval.json`. Local source bytes were verified against Git blob hashes.
- `freeze.json` fixes the protocol, mapping, cases, source/license, execution script, incremental monitor and oracle v2 before replay. Freeze SHA-256: `a42f765b371530d8794fcd0f41b52a84834d966c2cd7ab8a42e3b6c38c775a5d`.
- Replay: `python scp_revision/external_fixture/replay.py replay`, from the Paper 7 root. This verifies all frozen hashes before executing.

## Meaning of the result

The source supplied expected suppression outcomes; the Paper 7 adapter supplied preactivated traces and an exact-label-to-context mapping. Relative expiration time was preserved. The matching candidate is selected explicitly in the frozen mapping where the upstream test also retains a nonmatching silence. The four conditions were checked under their shared equality/expiration semantics.

This was a post-holdout, externally sourced fixture projection. The primary experiment remains unchanged. Alertmanager was not built or executed. The four source assertions are dependent steps of one upstream test, not independent industrial observations. They do not test policy-version changes, scheduled starts, regular expressions, or native handling of overlapping silences. The coverage ledger identifies lines 1419, 1426, 1436 and 1442 as outside native policy and records the exact reason for each.

The result supports interoperability of the selected suppression conditions at the mapped interface. It does not resolve the separate need for externally grounded evidence/policy revision histories and episode contracts.
