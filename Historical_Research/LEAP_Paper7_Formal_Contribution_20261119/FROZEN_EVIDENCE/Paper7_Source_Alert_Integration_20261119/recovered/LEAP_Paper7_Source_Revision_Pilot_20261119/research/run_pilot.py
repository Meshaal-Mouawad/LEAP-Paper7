#!/usr/bin/env python3
"""Portable re-execution of the native LEAP authorization audit and source proxy study.
Run from any directory after extracting the deliverable ZIP. No network, pip, or GPU required.
"""
import subprocess,sys,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
script=ROOT/'research'
EXPECTED_PROTOCOL_SHA256='a3540bed5ec7eb452cfb45d33b907838b6efd78a605de26f9d01406432c811c0'
actual=hashlib.sha256((script/'pre_registered_protocol.json').read_bytes()).hexdigest()
assert actual==EXPECTED_PROTOCOL_SHA256, 'Protocol file content differs from prespecified reference'
for name in ('audit_native_override.py','source_revision_proxy.py','propagate_through_monitor.py'):
    cmd=[sys.executable,str(script/name)]
    print('RUN',name,flush=True)
    subprocess.run(cmd,cwd=ROOT,check=True)
native=json.loads((ROOT/'analysis/native_override_test_results.json').read_text())
proxy=json.loads((ROOT/'analysis/proxy_summary.json').read_text())
bridge=json.loads((ROOT/'analysis/downstream_bridge_summary.json').read_text())
assert native['pass_count']==4 and native['fail_count']==6
assert proxy['cases']==24 and proxy['families']==4
assert proxy['reference_true']==14 and proxy['reference_false']==10
assert bridge['cases']==24
assert all(v['active_episode_differences']==0 for v in bridge['per_strategy'].values())
print('PORTABLE STUDY REPRODUCTION PASSED')
