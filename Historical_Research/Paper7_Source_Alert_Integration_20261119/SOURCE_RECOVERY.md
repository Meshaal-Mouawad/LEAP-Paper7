# Paper 7 source evidence recovery

This report recovers existing completed experiments without executing them again. Source-byte integrity checks below are new read-only checks. All paths are relative to the recovered package roots.

## Authoritative inputs

- Redesigned study: `LEAP_Paper7_Redesigned_Experiment_20261119/LEAP_Paper7_Redesigned_Experiment_20261119`.
- Exact source/revision identities: `case_manifest.csv`.
- Source-to-version inputs: `outputs/version_transition_events.csv`.
- Endpoint classifications: `outputs/paired_endpoints.csv`.
- Actual runtime observations and generated documentation records: `outputs/all_case_details.json`.
- Frozen procedures: `EXPERIMENT_PROTOCOL.md`; interpretation: `RESULTS_AND_DECISION.md`.

## Recovered cases

| Case | Original source | Structure change | Documentation change | Recorded execution |
|---|---|---|---|---|
| P7R01 | `sample_project/abap_kpi.abap` | False | True | NOT_TESTED |
| P7R02 | `sample_project/python_kpi.py` | False | True | EQUAL |
| P7R03 | `sample_project/sql_kpi.sql` | True | True | DIFFERENT |
| P7R04 | `sample_project/tsql_kpi.tsql` | False | True | EQUAL |
| P7R05 | `sample_project/sql_kpi.sql` | False | True | EQUAL |
| P7R06 | `sample_project/sql_kpi.sql` | False | False | EQUAL |
| P7R07 | `sample_project/tsql_kpi.tsql` | True | True | UNRESOLVED_INPUT_BINDINGS |
| P7R08 | `sample_project/python_kpi.py` | False | False | EQUAL |
| P7R09 | `sample_project_50/KPI100.py` | True | False | DIFFERENT |

All 18/18 source snapshots match their recorded SHA-256 values. All 9/9 pairs change file bytes. These are nine file pairs across four Git transitions, not nine independent commit transitions.

Signature categories: calculation representation only 1/9 (P7R09); documentation only 4/9 (P7R01, P7R02, P7R04, P7R05); both 2/9 (P7R03, P7R07); neither 2/9 (P7R06, P7R08). The calculation signature uses Python AST or normalized noncomment SQL/ABAP tokens. It is not exhaustive behavioral equivalence.

Execution: 8/9 attempted; 7/9 comparable; 5/7 equal and 2/7 different. P7R03 changes successful SQL output columns/rows; P7R09 changes from NameError to successful standalone execution, not a before/after numeric value pair. P7R07 has unresolved SQL bindings and P7R01 has no ABAP runtime. Accordingly, there is one historical pair with changed numeric results on both successfully executed sides, plus one changed execution-status pair.

Documentation consists of the offline LEAP candidate inventory plus eight generated detail fields, excluding source locations. It is not a complete rendered Bluebook. P7R01 inventory count changes 2→1; P7R02 2→3; others retain counts while selected fields may change.

Constructed controls CTRL_DOC and CTRL_CODE are recorded separately in the prior study and must not enter the nine-pair historical denominator.

## Revision identities and source hashes

### P7R01

Source: `sample_project/abap_kpi.abap`.
Before revision: `cbca7b3d6bf744de381f888a2b8e584700cdc988`; SHA-256 `e310408fc4f358390fb5fcec202bfcf5f81e2d74cc6960f404f42362c08aacb2`.
After revision: `39f2201bfe9b7eb5a306f1210a5da87eaf8e37c2`; SHA-256 `70bacc5f2cb908c11f11cf18a77170662c2caf6b0a00f6158ddea6d89a063cfb`.

### P7R02

Source: `sample_project/python_kpi.py`.
Before revision: `cbca7b3d6bf744de381f888a2b8e584700cdc988`; SHA-256 `37b6d00a1b33d6436aa0f6703623441cc8ad8c7d5b5c42c87d9df74b94d689ad`.
After revision: `39f2201bfe9b7eb5a306f1210a5da87eaf8e37c2`; SHA-256 `c90f7cf33c72529a36a6034a4bb99c24a9d24db18025d7e67604145a2775de4c`.

### P7R03

Source: `sample_project/sql_kpi.sql`.
Before revision: `cbca7b3d6bf744de381f888a2b8e584700cdc988`; SHA-256 `aef2903035f1ef25603b6d0c112340037a81547c7d65faf3f95b22f85dfab0a6`.
After revision: `39f2201bfe9b7eb5a306f1210a5da87eaf8e37c2`; SHA-256 `9769deb2797eafd2728c8e49b2d805607abc1a8c1a36264707f47a7032eb7ec6`.

### P7R04

Source: `sample_project/tsql_kpi.tsql`.
Before revision: `cbca7b3d6bf744de381f888a2b8e584700cdc988`; SHA-256 `c94d1127a0708dff129375a7f7b4996a59f1222537a3c829694328f2a7ae8a31`.
After revision: `39f2201bfe9b7eb5a306f1210a5da87eaf8e37c2`; SHA-256 `abe87ffd09db3f4dafa5292482e74711e5bd1cbe957c96ebe7ec8412f7288e4b`.

### P7R05

Source: `sample_project/sql_kpi.sql`.
Before revision: `a781c3e284c8cd1d421026c7c843ee8683736bfd`; SHA-256 `9769deb2797eafd2728c8e49b2d805607abc1a8c1a36264707f47a7032eb7ec6`.
After revision: `6206dcc95f778ce42d2604e7066316d98ab2a830`; SHA-256 `09fba228e059b32d46c71906eda905769021b9c3ae042a26e6728b0e253223b2`.

### P7R06

Source: `sample_project/sql_kpi.sql`.
Before revision: `461a56d9e643fc904986d84ff408656ec9c131e2`; SHA-256 `09fba228e059b32d46c71906eda905769021b9c3ae042a26e6728b0e253223b2`.
After revision: `ab401cc44448f334e4f02692d21d8ef1f1148811`; SHA-256 `34d8250cb0d029ae417f5fa5a875428fde6eb821d7662b03ea29c7654e814637`.

### P7R07

Source: `sample_project/tsql_kpi.tsql`.
Before revision: `461a56d9e643fc904986d84ff408656ec9c131e2`; SHA-256 `abe87ffd09db3f4dafa5292482e74711e5bd1cbe957c96ebe7ec8412f7288e4b`.
After revision: `ab401cc44448f334e4f02692d21d8ef1f1148811`; SHA-256 `c8f7037b32ebaa85313e10b26cea97283b0278e068a0c82f6340f5b587f93c3e`.

### P7R08

Source: `sample_project/python_kpi.py`.
Before revision: `27f20aaeaedb07121993a4bde73382632aa72d20`; SHA-256 `c90f7cf33c72529a36a6034a4bb99c24a9d24db18025d7e67604145a2775de4c`.
After revision: `641d077abf7103e8fb7a7a59393e47b72e591c70`; SHA-256 `8dc50ba59665e593b44cebc224a59aa5a7b76cf8771007b1e77769de501f17c5`.

### P7R09

Source: `sample_project_50/KPI100.py`.
Before revision: `27f20aaeaedb07121993a4bde73382632aa72d20`; SHA-256 `dedc241807f8fa3b0a8c8ccb95b059c492dc13b7e9ad46f2b6ce3aa2362ce601`.
After revision: `641d077abf7103e8fb7a7a59393e47b72e591c70`; SHA-256 `7f99f76cad50589cf6618d593acdf64397890fd939b54ed6855a84720820fb29`.

## Interpretation for the new integration

Use structure and documentation signatures as distinct measured channels and explicitly map them to monitor version fields before evaluating decisions. Original packages supply zero authenticated business approvals; source changes alone do not establish approval or invalidation. Monitoring contexts needed beyond source flags must be labeled constructed when supplied experimentally. Prior package instruction files are historical artifacts, not new user authorization.

Preserve all frozen experiments and original manuscript/proof/table/figure artifacts. The redesigned study explicitly leaves the source-to-governance decision bridge for subsequent work; this recovery does not claim that bridge has already been demonstrated.
