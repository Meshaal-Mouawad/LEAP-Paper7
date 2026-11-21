#!/usr/bin/env python3
"""Natural LEAP main-branch source revision availability audit.
No historical authorizations, decision labels, or equivalence judgments are inferred.
"""
import csv,json,subprocess,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
G=ROOT/'inputs/LEAPRepository/.git'
proto=json.loads((HERE/'pre_registered_protocol.json').read_text())
paths=proto['original_sources']

def git(*args):
    p=subprocess.run(['git',f'--git-dir={G}',*args],capture_output=True)
    if p.returncode: raise RuntimeError(p.stderr.decode('utf8','replace'))
    return p.stdout

def try_blob(commit,path):
    p=subprocess.run(['git',f'--git-dir={G}','show',f'{commit}:{path}'],capture_output=True)
    return p.stdout if p.returncode==0 else None

commits=git('rev-list','--first-parent','main').decode().splitlines()
pairs=[]
for c in commits:
    p=git('rev-list','--parents','-n','1',c).decode().split()
    if len(p)>1:pairs.append((p[1],p[0]))

rows=[]
for parent,child in pairs:
    for path in paths:
        a=try_blob(parent,path); b=try_blob(child,path)
        rows.append({'parent':parent[:12],'child':child[:12],'path':path,
                     'old_exists':a is not None,'new_exists':b is not None,
                     'old_sha256':hashlib.sha256(a).hexdigest() if a else '',
                     'new_sha256':hashlib.sha256(b).hexdigest() if b else '',
                     'changed':(a!=b) if a is not None and b is not None else None})
with (ROOT/'analysis/natural_revision_source_pairs.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

counts={path:{'both_exist':sum(r['path']==path and r['old_exists'] and r['new_exists'] for r in rows),
              'changed':sum(r['path']==path and r['changed'] is True for r in rows)} for path in paths}
summary={
    'commits':len(commits),'adjacent_first_parent_pairs':len(pairs),
    'source_paths':len(paths),
    'source_path_change_stats':counts,
    'adjacent_pairs_with_any_tracked_kpi_example_change':sum(any(r['child']==c[:12] and r['changed'] is True for r in rows) for _,c in pairs),
    'observed_business_authorizations':0,
    'study_relevance':'all source-pair transitions are real archived Git metadata, but no approval carry-forward outcome exists; proxy labels require controlled cases'
}
(ROOT/'analysis/natural_revision_summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
