# Paper 7 temporal study and strict-review verification

Extract the archive and enter `Paper7_Reproduction`. Use Python 3.11 or later with SQLite and pandas installed. The verified environment used Python 3.12.14, SQLite 3.53.1, and pandas 2.2.3. Once these prerequisites are available, all commands run offline.

```sh
python -B run_all.py ../paper7-run
```

Choose a fresh output directory outside the extracted package. The script preserves the extracted files. It records the command arguments and exit statuses in `commands.json`, separate command streams in `logs/`, the full replay and nine internal command records in `study_run/`, the independent endpoint tables in `analysis/`, and the taxonomy and targeted outputs in `review_run/strict_revision/method/`.

## Run each check individually

The four commands from the original package remain available. Run these from `Paper7_Reproduction`, choosing new destinations if rerunning.

```sh
python -B scripts/verify_package.py
python -B study/reproduce.py
python -B scripts/retain_replay.py study ../paper7-manual-run
python -B scripts/independent_audit.py ../paper7-manual-run ../paper7-manual-analysis
```

For the two post-study checks, prepare a separate copy of the supplied study using a fresh destination.

```sh
cp -R study ../paper7-manual-review
mkdir -p ../paper7-manual-review/strict_revision/method
cp -R review_checks/method/. ../paper7-manual-review/strict_revision/method/
cd ../paper7-manual-review
python -B strict_revision/method/audit_taxonomy.py
python -B strict_revision/method/run_targeted_checks.py
```

The first check verifies the ten offline freeze entries, reconstructs all 55 operation-index combinations, and compares all 825 intervention representations after time normalization. The second verifies the ten entries of the targeted fixture freeze and checks the final decision and reason of 24 cases across four implementations. Every implementation also emits the same complete sequence for each of the 24 traces, covering 75 events per implementation.

| Check | Verified result |
|---|---:|
| Frozen benchmark | 4,935 traces, 26,430 events |
| Held-out families | 987 base traces, 2,961 including transformations |
| Complete decisions without suppression binding | 957/987 exact base traces |
| Active intervals without suppression binding | 987/987 exact base traces |
| Reduced comparison representation | 585 reason differences and zero decision-sequence differences |
| Intervention reconstruction | 55 designs per family, 825/825 representations checked |
| Concurrent-condition verification | 24/24 cases, 96/96 final-output checks |
| Independent scoring | 270/270 original metric rows equal |

## Provenance and scope

[Reporting clarification](REPORTING_CLARIFICATION_20261118.md) records the scope of the family partition and the composition and timing of the corrected-reference checks.

The archive preserves every file of the original 174-entry `LEAP_Paper7_Research_Reproduction.zip`. That archive's SHA-256 is `c121f98da3a2379c56655f5511673f1018de121dcb71ad684018046a35b1c94c`. The preserved `PACKAGE_SHA256SUMS` verifies its 173 payload files, and `REVIEW_SHA256SUMS` verifies the additions. `study/SHA256SUMS` verifies 58 offline inputs. `study/protocol/FREEZE.json` is the existing offline integrity manifest. A separate verification with the historical material checked all 15 historical freeze entries. The historical and offline trace hashes and the projection reconciliation are recorded in `review_checks/provenance/FREEZE_VERIFICATION.json`.

This package starts at the temporal observation interface. The historical trace records project to the supplied temporal records by dropping 18,600 illustrative source snapshots and their corresponding hash fields. The reference sequence and all three raw prediction digests match the frozen outputs. The five rule families use the same 329 labeled temporal templates. Their source-rule identities and simulated source identifiers define the development and held-out partitions. The two transformations stay in their original family-design group.

The taxonomy and targeted-case code comes unchanged from the strict review. The targeted cases are retrospective checks outside the frozen benchmark denominator. The unchanged original AI activity record documents the separate reference-authoring assignment and the scoring process in `review_checks/provenance/AI_ACTIVITY_RECORD.json`. Replay and raw rescoring are deterministic software checks of constructed traces. Private adapter source recovery, the source snapshots, and human or deployment validation are outside this bundle's scope.
