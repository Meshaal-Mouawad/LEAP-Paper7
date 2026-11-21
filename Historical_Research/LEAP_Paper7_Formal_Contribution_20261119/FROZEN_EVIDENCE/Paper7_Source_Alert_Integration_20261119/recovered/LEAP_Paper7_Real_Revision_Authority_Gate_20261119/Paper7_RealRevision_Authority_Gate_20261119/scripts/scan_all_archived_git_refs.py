#!/usr/bin/env python3
"""Optional read-only real-source-history scanner (requires original .git).
Usage: python scripts/scan_all_archived_git_refs.py --git-dir /path/to/.git --out scan.csv
Does not generate approval decisions.
"""
import argparse,subprocess,csv,re,collections
p=argparse.ArgumentParser();p.add_argument('--git-dir',required=True);p.add_argument('--out',required=True);args=p.parse_args()
def git(*a):
 r=subprocess.run(['git','--git-dir='+args.git_dir,*a],capture_output=True,text=True)
 if r.returncode:raise RuntimeError(r.stderr)
 return r.stdout
allc=git('rev-list','--all').splitlines();rows=[];edges=0
for c in allc:
 parents=git('rev-list','--parents','-n','1',c).split()[1:]
 for parent in parents:
  edges+=1
  for line in git('diff','--name-status','--no-renames',parent,c,'--','*.py','*.sql','*.tsql','*.abap','*.r','*.ipynb','*.sas').splitlines():
   status,path=line.split('\t',1)
   if any(x in path for x in ('/.venv/','/site-packages/','/__pycache__/')):continue
   rows.append({'parent':parent,'child':c,'path':path,'status':status})
with open(args.out,'w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['parent','child','path','status']);w.writeheader();w.writerows(rows)
print(f'commits={len(allc)} parent_edges={edges} source_status_events={len(rows)} modified_example_pairs={sum(r["status"]=="M" and r["path"].startswith("sample") for r in rows)}')
