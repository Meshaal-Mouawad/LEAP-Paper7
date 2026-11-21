"""Replay the frozen temporal study and its post-study verification checks."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).resolve().parent


def verify_review_files():
    manifest = ROOT / 'REVIEW_SHA256SUMS'
    for line in manifest.read_text().splitlines():
        expected, name = line.split('  ', 1)
        with (ROOT / name).open('rb') as stream:
            actual = hashlib.file_digest(stream, 'sha256').hexdigest()
        if actual != expected:
            raise ValueError(f'Review file checksum mismatch: {name}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path, help='A new, empty-by-construction run directory')
    output = parser.parse_args().output.resolve()
    if output.is_relative_to(ROOT):
        parser.error('Put the run directory outside the extracted reproduction package.')
    output.mkdir(parents=True)
    logs = output / 'logs'
    logs.mkdir()
    commands = []

    def run(label, cwd, *arguments):
        command = [sys.executable, '-B', *map(str, arguments)]
        result = subprocess.run(command, cwd=cwd, capture_output=True)
        (logs / f'{label}.stdout.log').write_bytes(result.stdout)
        (logs / f'{label}.stderr.log').write_bytes(result.stderr)
        commands.append(dict(name=label, argv=command, working_directory=str(cwd),
                             exit_code=result.returncode))
        (output / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n')
        print(f'{label}: exit {result.returncode}', flush=True)
        result.check_returncode()

    verify_review_files()
    run('package_verify', ROOT, 'scripts/verify_package.py')
    run('documented_replay', ROOT, 'study/reproduce.py')
    study_run = output / 'study_run'
    run('retained_replay', ROOT, 'scripts/retain_replay.py', 'study', study_run)
    run('independent_audit', ROOT, 'scripts/independent_audit.py', study_run, output / 'analysis')

    review_run = output / 'review_run'
    shutil.copytree(ROOT / 'study', review_run)
    shutil.copytree(ROOT / 'review_checks/method', review_run / 'strict_revision/method')
    run('taxonomy_audit', review_run, 'strict_revision/method/audit_taxonomy.py')
    run('targeted_checks', review_run, 'strict_revision/method/run_targeted_checks.py')


if __name__ == '__main__':
    main()
