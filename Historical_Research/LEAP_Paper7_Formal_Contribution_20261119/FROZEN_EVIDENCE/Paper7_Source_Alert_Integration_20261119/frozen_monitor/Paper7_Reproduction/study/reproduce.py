"""Verify the Paper 7 supplement and regenerate its deterministic outputs offline."""

import hashlib
import json
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def read_json(path):
    return json.loads(path.read_text())


def sha256(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def require_equal(actual, expected, label):
    if actual != expected:
        raise RuntimeError(f'{label} differs from the reference')


def run(root, script, *args):
    result = subprocess.run(
        [sys.executable, '-B', script, *args], cwd=root, capture_output=True, text=True
    )
    if result.returncode:
        raise RuntimeError(f'{script} failed\n{result.stdout}{result.stderr}')
    return result.stdout


def read_without(path, runtime_keys):
    record = read_json(path)
    for key in runtime_keys:
        record.pop(key)
    return record


def verify_references(root, trace_total, event_total):
    sys.path.insert(0, str(root / 'implementation'))
    sys.dont_write_bytecode = True
    from oracle import oracle as historical_oracle
    from oracle_v2 import oracle as corrected_oracle

    benchmark = root / 'benchmark'
    policy = read_json(benchmark / 'policy.json')
    count = events = 0
    with (benchmark / 'traces.jsonl').open() as traces, (benchmark / 'reference.jsonl').open() as references:
        for trace_line, reference_line in zip(traces, references, strict=True):
            trace, reference = json.loads(trace_line), json.loads(reference_line)
            require_equal(trace['id'], reference['id'], 'reference identifier')
            inputs = (trace['trace'], policy, trace['severity'])
            for oracle in (historical_oracle, corrected_oracle):
                require_equal(oracle(*inputs), reference['outputs'], f"{oracle.__module__} {trace['id']}")
            count += 1
            events += len(trace['trace'])
    require_equal((count, events), (trace_total, event_total), 'oracle sample size')


def json_lines(path):
    with path.open() as stream:
        yield from map(json.loads, stream)


def verify_pycontract(root, expected, hashes):
    baseline = root / 'r3/baseline'
    sys.path.insert(0, str(baseline))
    from pycontract_baseline import pc, validate

    engine = Path(sys.modules[pc.Monitor.__module__].__file__).resolve()
    require_equal(engine, baseline / 'upstream/pycontract/pycontract_core.py', 'PyContract engine path')
    for record in read_json(baseline / 'upstream/VERIFIED_SOURCE.json'):
        require_equal(sha256(baseline / 'upstream' / record['path']), record['sha256'], record['path'])

    policy = read_json(root / 'benchmark/policy.json')
    digest = hashlib.sha256()
    for record in json_lines(root / 'benchmark/traces.jsonl'):
        events, durations = validate(record['trace'], policy)
        normalized = dict(id=record['id'], trace=events, policy=durations, severity=record['severity'])
        canonical = json.dumps(normalized, sort_keys=True, separators=(',', ':'))
        digest.update((canonical + '\n').encode())
    require_equal(
        digest.hexdigest(), hashes['pycontract_original_normalized_inputs_sha256'],
        'normalized PyContract input projection',
    )

    run(root, 'r3/baseline/run_baseline.py')
    require_equal(
        read_without(baseline / 'summary.json', ('utc_started', 'elapsed_seconds', 'runtime')),
        read_json(expected / 'pycontract_metrics.json'), 'PyContract metrics',
    )
    for name, original_digest in hashes['pycontract_outputs_sha256'].items():
        require_equal(sha256(baseline / name), original_digest, f'PyContract {name}')

    primary = json_lines(root / 'results/predictions.jsonl')
    complete = (record for record in primary if record['method'] == 'bound')
    external = json_lines(baseline / 'predictions.jsonl')
    traces = events = 0
    for full, baseline_record in zip(complete, external, strict=True):
        trace_id = full['id']
        require_equal(baseline_record['id'], trace_id, 'PyContract trace identifier')
        require_equal(baseline_record['outputs'], full['outputs'], f'PyContract versus full {trace_id}')
        audit = baseline_record['engine_audit']
        count = len(full['outputs'])
        require_equal(audit['engine_events'], count, f'engine events {trace_id}')
        require_equal(audit['state_transitions'], count, f'engine transitions {trace_id}')
        require_equal(len(audit['state_classes']), count, f'engine states {trace_id}')
        traces += 1
        events += count
    require_equal((traces, events), (hashes['traces'], hashes['events']), 'PyContract sample size')
    run(root, 'r3/baseline/verify_engine_dependency.py')
    require_equal(
        read_json(baseline / 'engine_dependency_checks.json'),
        read_json(expected / 'pycontract_engine_dependency.json'), 'PyContract dispatch dependency',
    )
    return digest.hexdigest()


def reproduce(root):
    expected = root / 'expected'
    hashes = read_json(expected / 'output_hashes.json')
    require_equal(sha256(root / 'benchmark/traces.jsonl'), hashes['supplement_traces_sha256'], 'trace archive')
    verify_references(root, hashes['traces'], hashes['events'])

    run(root, 'implementation/evaluate.py', 'results')
    require_equal(
        read_without(root / 'results/summary.json', ('runtime_seconds', 'environment', 'freeze_sha256')),
        read_json(expected / 'primary_metrics.json'), 'primary metrics',
    )
    require_equal(sha256(root / 'results/predictions.jsonl'), hashes['primary_predictions_sha256'], 'primary predictions')
    run(root, 'implementation/audit_information_bound.py')
    for name in ('information_classes', 'information_bound'):
        require_equal(sha256(root / f'results/{name}.json'), hashes[f'{name}_sha256'], name)

    equality = json.loads(run(root, 'scp_revision/equality/verify.py'))
    require_equal(equality, {'traces': hashes['traces'], 'events': hashes['events'], 'mismatched_sequences': 0}, 'equality replay')
    representation = json.loads(run(root, 'r3/analysis/representation.py'))
    require_equal(representation, read_json(expected / 'representation_results.json'), 'R3 representation replay')

    run(root, 'replication_r2/run_replication.py')
    require_equal(
        read_without(root / 'replication_r2/summary.json', ('utc_started', 'elapsed_seconds', 'runtime')),
        read_json(expected / 'sqlite_metrics.json'), 'SQLite metrics',
    )
    require_equal(sha256(root / 'replication_r2/predictions.jsonl'), hashes['sqlite_predictions_sha256'], 'SQLite predictions')
    pycontract_projection = verify_pycontract(root, expected, hashes)

    run(root, 'reviews/check_reference_v2.py')
    checks = read_json(root / 'reviews/reference_checks_v2.json')
    require_equal((checks['passed'], checks['total']), (29, 29), 'oracle regression checks')

    run(root, 'scp_revision/external_fixture/replay.py', 'replay')
    require_equal(
        read_without(root / 'scp_revision/external_fixture/results.json', ('run_at_utc', 'platform', 'python')),
        read_json(expected / 'fixture_results.json'), 'Alertmanager projection',
    )

    return {
        'python': sys.version.split()[0],
        'sqlite': sqlite3.sqlite_version,
        'traces': hashes['traces'],
        'events': hashes['events'],
        'exact_prediction_files': ['primary', 'SQLite', 'PyContract'],
        'pycontract_normalized_projection_sha256': pycontract_projection,
        'oracle_regression_checks': checks['passed'],
        'equality_mismatches': equality['mismatched_sequences'],
        'representation': representation,
        'mapped_alertmanager_expectations': 4,
    }


if __name__ == '__main__':
    for line in (ROOT / 'SHA256SUMS').read_text().splitlines():
        expected_hash, name = line.split('  ', 1)
        require_equal(sha256(ROOT / name), expected_hash, name)
    with tempfile.TemporaryDirectory(prefix='paper7-offline-') as directory:
        work = Path(directory) / 'supplement'
        shutil.copytree(ROOT, work)
        print(json.dumps(reproduce(work), indent=2))
