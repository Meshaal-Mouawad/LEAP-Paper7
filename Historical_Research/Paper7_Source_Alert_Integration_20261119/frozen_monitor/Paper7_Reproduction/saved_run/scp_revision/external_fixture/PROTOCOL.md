# External fixture projection — pre-replay protocol

Paper 7, revision 2. Date: 2026-11-18. This small post-holdout supplement imports externally authored expected suppression outcomes. It does not modify the frozen main benchmark, models, estimates or protocol.

Source: Prometheus Alertmanager v0.28.1, `silence/silence_test.go`, `TestSilencer`, lines 1372–1443. Source and Apache-2.0 license were retrieved through the authenticated GitHub connector. Full source bytes and license are preserved; Git blob hashes and SHA-256 hashes are verified in `source/retrieval.json`.

## Selection and reference

Select the first four of the eight `s.Mutes` assertions in this test: absence of a silence, a nonmatching exact matcher, a matching exact matcher, and expiration of the matching silence. Expected outcomes are read from the source assertions before running Paper 7. All eight assertions remain in the coverage ledger. Later assertions involving scheduled activation, overlapping silences, and a regular-expression matcher are marked outside the native Paper 7 policy. They are not excluded errors or successes.

## Projection

The fixed alert label is `foo=bar`. Encode its value as current context `bar`, and a selected exact matcher's pattern as suppression context (`baz` or `bar`). The context strings are adapter values for this fixture exercise, not evidence that Alertmanager itself has Paper 7 source-context semantics. Use fixed matching policy `P0` for the alert, observation and suppression; the external test supplies no policy-version mutation. Map the source test's initial `now` to 3 seconds, preserving relative ends (+300 seconds) and the expiration query (+3600 seconds).

Each case is an independent Paper 7 trace. Positive observations at 0 and 2 seconds establish an active episode; a fresh positive observation is supplied at the query time. This is an explicit adapter setup, not an imported upstream lifecycle trace. Keep the original Paper 7 D=C=F=2, E=4 seconds. Consequently, an expired suppression queried after one hour may display ESCALATED; the external assertion compares suppression, not severity.

At source assertion 3, both sil1 (foo=baz) and sil2 (foo=bar) exist; the fixed-label projection discards the nonmatching sil1 and retains sil2. Assertion 4 retains that matching sil2 after expiration. This reduction is justified only for the source's fixed alert label and these four assertions. Native multi-silence matching is not claimed.

The adapter does not consult expected outcomes. Case-to-silence selection, times, observations, and projection are frozen before replay. Source reference is a Boolean `Mutes` expectation. Paper 7 mapped output is `state == SUPPRESSED` at the final event. Verify the episode is active before and during the query, and verify complete Paper 7 output against independent oracle v2. Preserve full output and source line reference for every case.

## Freeze and scoring

Before replay, freeze this protocol, source, license, mapping, generated cases, replay code, monitor, and oracle v2 by SHA-256 in `freeze.json`. Replay aborts if any frozen input differs. Primary result is the count of four mapped source assertions whose suppression output agrees. Also report upstream coverage 4/8, unmapped 4/8, execution failures, full monitor/oracle agreement and active-episode setup checks. Four dependent assertions from one upstream test are a conformance check; they supply no statistical sample or independent industrial cases. No Alertmanager build, upstream test execution, or deployment is performed.
