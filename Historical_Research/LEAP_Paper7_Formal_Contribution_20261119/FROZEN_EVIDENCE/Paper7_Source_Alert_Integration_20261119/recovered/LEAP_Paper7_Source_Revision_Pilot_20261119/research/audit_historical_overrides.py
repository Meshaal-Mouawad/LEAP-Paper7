#!/usr/bin/env python3
"""Read-only historical Git inventory for authored overrides and authorization provenance.
No contents are interpreted as signed approvals without corresponding metadata.
"""
import json,subprocess,hashlib,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
G=ROOT/'inputs/LEAPRepository/.git'
if not G.is_dir():
    raise SystemExit('Full archive Git objects required for historical scan; see precomputed results in analysis/')

def git(*args):
    p=subprocess.run(['git',f'--git-dir={G}',*args],capture_output=True)
    return p.stdout,p.returncode
commits=git('rev-list','--all')[0].decode().splitlines()
paths=['kb/overrides.json','bluebook_generator/kb/overrides.json','docs/governance_overrides.json','docs/overrides.json']
rows=[]; hashes={}
for c in commits:
 for path in paths:
  out,rc=git('show',f'{c}:{path}')
  if rc: continue
  try:j=json.loads(out)
  except Exception:continue
  if not isinstance(j,dict):continue
  entries=j if path=='docs/overrides.json' else j.get('kpis',{})
  if not isinstance(entries,dict) or not entries:continue
  sha=hashlib.sha256(out).hexdigest()
  hashes.setdefault((path,sha),[]).append(c)
  for key,record in entries.items():
   if not isinstance(record,dict):continue
   fields=set(record)
   # fields objective/description/comments are definitions, not an authorization audit trail
   evidence_keys=[k for k in fields if k.lower() in ('approved_by','approver','approval_at','timestamp','file_signature','code_hash','approval_id','status','expires_at','deferral_id')]
   rows.append({'commit':c[:12],'path':path,'file_sha256':sha,'entry_key':key,
       'approval_provenance_fields':';'.join(sorted(evidence_keys)),
       'qualifies_as_verifiable_authorization':bool({'approved_by','approval_at','file_signature','status'}.issubset(fields))})
report={'full_git_commit_count':len(commits), 'nonempty_snapshot_pairs':len(hashes),
        'nonempty_snapshots_with_commits':{f'{path}@{sha[:12]}':len(cs) for (path,sha),cs in hashes.items()},
        'unique_authored_entries':sorted(set(r['entry_key'] for r in rows)),
        'found_authorization_provenance_entries':sum(r['qualifies_as_verifiable_authorization'] for r in rows),
        'rows_nonempty':len(rows),
        'status':'Real historical override text exists on non-main branches; independent human authorization and cross-revision status not established'}
(ROOT/'analysis/historical_override_discovery.json').write_text(json.dumps(report,indent=2))
with (ROOT/'analysis/historical_overrides_provenance.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
print(json.dumps(report,indent=2))
