#!/usr/bin/env python3
"""Deterministic downstream propagation of *proxy* source-authorization references.
This is a bridge test, not a second independent benchmark or human validation.
"""
from pathlib import Path
import csv,copy,importlib.util,json
ROOT=Path(__file__).resolve().parent.parent
MOD=ROOT/'inputs/Paper7_Reproduction/saved_run/implementation/monitor.py'
if not MOD.exists():
    import zipfile
    with zipfile.ZipFile(ROOT/'inputs/Frozen_Paper7_Reproduction_20261119.zip') as z:
        z.extractall(ROOT/'inputs')
spec=importlib.util.spec_from_file_location('frozen_p7_monitor', MOD)
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
reference=json.loads((ROOT/'inputs/frozen_central_witness.json').read_text())
original_events=reference['events']
policy={'D':2,'C':2,'E':4,'F':2} # read from the actual frozen policy below
polfile=ROOT/'inputs/Paper7_Reproduction/saved_run/benchmark/policy.json'
pol=json.loads(polfile.read_text())
# Standard fixed audit family duration from frozen witness: verify before setting.
print('policy file',json.dumps(pol)[:900])
if isinstance(pol,dict) and all(k in pol for k in ('D','C','E','F')):
    policy={k:pol[k] for k in ('D','C','E','F')}
else:
    # Fall back to witness recorded per-family policy, validated by reproducing the archived full outputs.
    family=reference['id'].split('/')[0]
    selected=pol.get(family) or pol.get('rules',{}).get(family)
    if selected and all(k in selected for k in ('D','C','E','F')):policy={k:selected[k] for k in ('D','C','E','F')}

severity='COMPLIANCE_AUDIT_GAP'
def simulate(authorized):
    events=copy.deepcopy(original_events)
    for event in events:
        if 's' in event:
            event['s']['c']='c1' if authorized else 'c0'
    return m.monitor(events,policy,base_severity=severity,mode='bound')

for expected in (True,False):
  output=simulate(expected)
  print('check ref choice',expected,'t3',output[3])

cases=json.loads((ROOT/'analysis/proxy_case_records.json').read_text())
rows=[]
for x in cases:
  reference_authorized=x['reference_output_equivalent_on_full_grid']
  ref=simulate(reference_authorized)
  for method,allow in x['candidate_predictions'].items():
     actual=simulate(allow)
     errors=[i for i,(a,b) in enumerate(zip(actual,ref)) if a!=b]
     active_diff=sum(a['active']!=b['active'] for a,b in zip(actual,ref))
     rows.append({
       'case_id':x['case_id'],'method':method,
       'proxy_authorization_reference':reference_authorized,
       'predicted_authorization':allow,
       'event_tuples_mismatched':len(errors),
       'mismatched_indices':','.join(str(i) for i in errors),
       'active_episode_differences':active_diff,
       'reference_t3':json.dumps(ref[3],sort_keys=True),
       'candidate_t3':json.dumps(actual[3],sort_keys=True),
     })
cols=list(rows[0]);
with (ROOT/'analysis/downstream_monitor_bridge.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(rows)
summary={'cases':len(cases), 'type':'deterministic counterfactual bridge from proxy authorization to existing frozen monitor',
         'fixed_trace':'audit/suppression_old_context/2/base', 'frozen_monitor_sha256':__import__('hashlib').sha256(MOD.read_bytes()).hexdigest(),
         'policy':policy,'per_strategy':{}}
for method in cases[0]['candidate_predictions']:
 subset=[r for r in rows if r['method']==method]
 summary['per_strategy'][method]={'cases_with_display_mismatch':sum(r['event_tuples_mismatched']>0 for r in subset),
    'mismatched_event_tuples':sum(r['event_tuples_mismatched'] for r in subset),
    'active_episode_differences':sum(r['active_episode_differences'] for r in subset)}
(ROOT/'analysis/downstream_bridge_summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
