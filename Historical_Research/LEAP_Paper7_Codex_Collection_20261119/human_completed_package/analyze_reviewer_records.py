#!/usr/bin/env python3
"""Analyze supplied signed reviewer records; do not generate decisions.
python -B analyze_reviewer_records.py --packet . --output NEW_DIRECTORY
"""
import argparse,csv,json,collections
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
def read(n):
 with (a.packet/n).open(newline='') as f:return list(csv.DictReader(f))
cases=read('collection_manifest.csv');reviews=read('adjudication_blind.csv');approvals=read('authentic_approval_records.csv')
ids={x['pair_id'] for x in cases};slots={};errors=[];complete={};distribution=collections.Counter()
for i,r in enumerate(reviews,2):
 key=(r['pair_id'],r['reviewer_code'])
 if key in slots:errors.append('Duplicate reviewer slot at row '+str(i))
 slots[key]=r
 if key[0] not in ids:errors.append('Unknown case at row '+str(i))
 d=r['initial_decision'].strip()
 if not d:continue
 if d not in {'KEEP','REVOKE','UNKNOWN'}:errors.append('Invalid decision at row '+str(i));continue
 if not r['manual_signature_reference'].strip() or not r['decision_timestamp'].strip():errors.append('Decision lacks signature reference or date at row '+str(i));continue
 if not r['reason'].strip():errors.append('Decision lacks reason at row '+str(i));continue
 complete[key]=r;distribution[d]+=1
paired=[]
for case in sorted(ids):
 if (case,'R1') in complete and (case,'R2') in complete:
  x=complete[(case,'R1')]['initial_decision'];y=complete[(case,'R2')]['initial_decision'];paired.append((case,x,y,x==y))
n=len(paired);agree=sum(x[3] for x in paired)
observed=agree/n if n else None;kappa=None
if n:
 left=collections.Counter(x[1] for x in paired);right=collections.Counter(x[2] for x in paired)
 expected=sum(left[k]*right[k] for k in {'KEEP','REVOKE','UNKNOWN'})/(n*n)
 if expected<1:kappa=(observed-expected)/(1-expected)
result={'historical_source_pairs':len(cases),'source_snapshots':2*len(cases),'constructed_pilot_cases':len(read('constructed_pilot/recorded_case_inventory.csv')),'approval_records':len(approvals),'reviewer_slots':len(reviews),'signed_review_decisions':len(complete),'cases_with_two_signed_decisions':n,'initial_agreements':agree if n else None,'initial_disagreements':n-agree if n else None,'observed_agreement':observed,'cohens_kappa_three_categories':kappa,'decision_distribution':dict(distribution),'validation_errors':errors,'analysis_state':'REVIEW_DATA_AVAILABLE' if n and not errors else 'REVIEW_DATA_REQUIRED','note':'Blank decisions remain blank; UNKNOWN is an explicit reviewer decision only. Agreement uses paired initial decisions, preserving disagreements before resolution.'}
a.output.mkdir(parents=True,exist_ok=False)
(a.output/'reviewer_analysis.json').write_text(json.dumps(result,indent=2)+'\n')
with (a.output/'paired_initial_decisions.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['pair_id','reviewer_R1_initial','reviewer_R2_initial','agreement']);w.writerows(paired)
print(json.dumps(result))
if errors:raise SystemExit(2)
