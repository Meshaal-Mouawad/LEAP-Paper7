#!/usr/bin/env python3
"""Targeted checks for Paper 7 candidate lemmas; never rewrites frozen records."""
import csv, importlib.util, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/'FROZEN_EVIDENCE/Paper7_Source_Alert_Integration_20261119'
MOD=E/'frozen_monitor/Paper7_Reproduction/study/implementation/monitor.py'
spec=importlib.util.spec_from_file_location('frozen_monitor',MOD)
monitor=importlib.util.module_from_spec(spec);spec.loader.exec_module(monitor)
POLICY=json.loads((E/'frozen_monitor/Paper7_Reproduction/saved_run/benchmark/policy.json').read_text())
assert all(POLICY[x]==v for x,v in dict(D=2,C=2,E=4,F=2).items())
rows={r['case_id']:r for r in csv.DictReader((E/'integration/outputs/pair_categories.csv').open())}
changes={(r['case_id'],r['strategy']):r['detected_change']=='True' for r in csv.DictReader((E/'integration/outputs/change_detection.csv').open())}
assert len(rows)==9 and len(changes)==36
assert rows['P7R01']['category']=='documentation_only' and rows['P7R06']['category']=='neither' and rows['P7R09']['category']=='calculation_representation_only'

def ev(t,c='c0',p='p0',value=True,at=None,obs=True,s=None):
 e={'t':t,'unit':'s','c':c,'p':p}
 if obs:e['o']={'at':t if at is None else at,'value':value,'c':c,'p':p}
 if s is not None:e['s']=s
 return e

def simple(change):
 return [ev(0),ev(2),ev(3,c='c1' if change else 'c0'),ev(5,c='c1' if change else 'c0')]

# Canonical version names isolate equality patterns. The actual monitor treats names as opaque.
patterns={str(c)+str(d):{'C':bool(c),'D':bool(d),'OR':bool(c or d),
 'reference':monitor.monitor(simple(bool(c or d)),POLICY)} for c in (0,1) for d in (0,1)}
assert patterns['00']['reference'][2]['state']=='ACTIVE'
assert all(patterns[k]['reference'][2]['state']=='PENDING' for k in ('01','10','11'))

def required(cid):
 r=rows[cid]
 return r['calculation_representation_changed']=='True' or r['documentation_changed']=='True'

witnesses=[]
for strategy,a,b in [('A_file','P7R01','P7R06'),('B_calculation','P7R01','P7R06'),('C_documentation','P7R09','P7R06')]:
 assert changes[(a,strategy)]==changes[(b,strategy)]
 assert required(a) and not required(b)
 projection=changes[(a,strategy)]
 obs=monitor.monitor(simple(projection),POLICY)
 ra=monitor.monitor(simple(required(a)),POLICY)
 rb=monitor.monitor(simple(required(b)),POLICY)
 assert ra[2]['state']=='PENDING' and rb[2]['state']=='ACTIVE'
 witnesses.append({'strategy':strategy,'archived_source_pairs':[a,b],
  'constructed_history':'fresh positive observations at t=0,2,3,5 seconds; source transition at t=3',
  'same_strategy_change_indicator':projection,'strategy_t3_output':obs[2],
  'dual_reference_t3_first':ra[2],'dual_reference_t3_second':rb[2],
  'different_required_decision':ra[2]['state']!=rb[2]['state']})

# Test temporal branches on the preserved monitor, using fresh constructed events.
base=[ev(0),ev(2)]
def tail(x):return monitor.monitor(base+[x],POLICY)[-1]
def check(name,event,expect):
 out=tail(event)
 for k,v in expect.items():assert out[k]==v,(name,k,out,v)
 return {'name':name,'expected':expect,'actual':out,'pass':True}
checks=[]
checks.append(check('context reset',ev(3,c='c1'),{'state':'PENDING','active':False,'reason':'CONTEXT_CHANGE'}))
checks.append(check('policy reset',ev(3,p='p1'),{'state':'PENDING','active':False,'reason':'POLICY_CHANGE'}))
checks.append(check('both changes policy precedence',ev(3,c='c1',p='p1'),{'reason':'POLICY_CHANGE'}))
checks.append(check('future observation',ev(3,at=4),{'state':'UNKNOWN','active':True,'reason':'FUTURE'}))
checks.append(check('stale observation',ev(3,at=0),{'state':'UNKNOWN','active':True,'reason':'STALE'}))
checks.append(check('freshness equality',ev(3,at=1),{'state':'ACTIVE','active':True,'reason':'STATE'}))
checks.append(check('missing precedence',ev(3,obs=False),{'reason':'MISSING','active':True}))
checks.append(check('conflict',ev(3,value=None),{'reason':'CONFLICT','active':True}))
x=ev(3,c='c1',p='p1',at=4,value=None);x['o'].update(c='c0',p='p0')
checks.append(check('concurrent faults context precedence',x,{'reason':'CONTEXT_MISMATCH','active':False}))
x=ev(3,p='p1',at=4,value=None);x['o']['p']='p0'
checks.append(check('policy mismatch precedes time faults',x,{'reason':'POLICY_MISMATCH','active':False}))
checks.append(check('mismatched deferral',ev(3,s={'c':'old','p':'p0','until':8}),{'state':'ACTIVE','active':True,'reason':'STATE'}))
checks.append(check('matching deferral before expiry',ev(3,s={'c':'c0','p':'p0','until':8}),{'state':'SUPPRESSED','active':True,'reason':'SUPPRESSION'}))
checks.append(check('expiry at event boundary',ev(3,s={'c':'c0','p':'p0','until':3}),{'state':'ACTIVE','active':True,'reason':'STATE'}))
checks.append(check('deferral policy mismatch',ev(3,s={'c':'c0','p':'old','until':8}),{'state':'ACTIVE','active':True,'reason':'STATE'}))

# Output-relative source partition for the fixed OR-reset contract; this is a finite lemma check.
partition={'00':'no reset','01':'reset','10':'reset','11':'reset'}
assert len(set(partition.values()))==2
for k,v in patterns.items():assert (v['reference'][2]['state']=='PENDING')==(partition[k]=='reset')
result={'provenance':{'source_rows':'integration/outputs/pair_categories.csv','change_rows':'integration/outputs/change_detection.csv','monitor':str(MOD.relative_to(ROOT))},
 'scope':'targeted finite checks of source patterns, three archived-pair witnesses, and 14 temporal branches; not a universal proof',
 'source_pattern_partition':partition,'witnesses':witnesses,'temporal_checks':checks,
 'counts':{'archived_pairs_read':len(rows),'witnesses':len(witnesses),'temporal_checks':len(checks)}}
(ROOT/'COUNTEREXAMPLES_AND_CHECKS/results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result['counts'],sort_keys=True))
