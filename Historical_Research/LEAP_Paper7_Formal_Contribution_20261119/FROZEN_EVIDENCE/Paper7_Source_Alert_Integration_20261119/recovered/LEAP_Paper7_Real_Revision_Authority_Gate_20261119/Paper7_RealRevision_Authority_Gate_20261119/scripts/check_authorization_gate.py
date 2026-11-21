#!/usr/bin/env python3
"""Authorization gate check. Refuses to score when approval/review evidence is missing."""
import csv,json,collections,sys
from pathlib import Path
root=Path(__file__).resolve().parent.parent
records=list(csv.DictReader((root/'data/real_source_revisions.csv').open()))
apps=list(csv.DictReader((root/'data/authenticated_authorizations_blank.csv').open()))
judgments=list(csv.DictReader((root/'data/reviewer_adjudication_blind.csv').open()))
bycase=collections.defaultdict(list)
for x in judgments:
 if x['adjudicator_id'] and x['decision_KEEP_REVOKE_UNKNOWN'] in {'KEEP','REVOKE','UNKNOWN'}:bycase[x['case_id']].append(x)
appbycase={x['case_id']:x for x in apps if x.get('original_approval_id') and x.get('approval_evidence_sha256') and x.get('record_is_authentic')=='true'}
ready=[]
for x in records:
 rs=bycase.get(x['case_id'],[])
 if x['case_id'] not in appbycase:continue
 if len(rs)<2 or len({r['adjudicator_id'] for r in rs})<2:continue
 if len({r['decision_KEEP_REVOKE_UNKNOWN'] for r in rs})>1:continue
 if rs[0]['decision_KEEP_REVOKE_UNKNOWN']=='UNKNOWN':continue
 ready.append(x['case_id'])
result={'status':'BLOCKED' if not ready else 'ELIGIBLE_REFERENCES_PRESENT_VERIFY_MANUALLY','real_source_change_pairs':len(records),'authenticated_approval_pairs':len(appbycase),'dual_consensus_decisions':len(ready),'research_claim':'No approval accuracy can be calculated unless every scored case has authenticated approval evidence and two genuine qualified human adjudications.'}
(root/'data/authorization_gate_status.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
if not ready:sys.exit(2)
