"""Hand-derived policy checks for the independently written oracle."""
from pathlib import Path
import sys,json,hashlib
sys.dont_write_bytecode=True
base=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(base/'implementation'))
from oracle_v2 import oracle
P={'D':2,'C':2,'E':4,'F':2}

def e(t,v=True,**kw):
    c=kw.pop('c','c1'); p=kw.pop('p','p1')
    event={'t':t,'c':c,'p':p,'unit':'s','o':{'value':v,'c':c,'p':p,'at':t}}
    event.update(kw)
    return event

def expected(states,actives=None,reasons=None):
    actives=actives or [s in ('ACTIVE','ESCALATED','SUPPRESSED') for s in states]
    reasons=reasons or ['SUPPRESSION' if s=='SUPPRESSED' else 'STATE' for s in states]
    return [dict(state=s,active=a,severity=('High' if s=='ACTIVE' else 'HIGH' if s=='ESCALATED' else 'UNKNOWN' if s=='UNKNOWN' else 'NONE'),reason=r) for s,a,r in zip(states,actives,reasons)]

cases=[]
def add(name,trace,states,actives=None,reasons=None,policy=P):
    cases.append((name,trace,policy,expected(states,actives,reasons)))
add('inclusive_dwell_and_escalation',[e(0),e(1),e(2),e(5),e(6)],['PENDING','PENDING','ACTIVE','ACTIVE','ESCALATED'])
add('inclusive_clear',[e(0),e(2),e(3,False),e(4,False),e(5,False)],['PENDING','ACTIVE','ACTIVE','ACTIVE','CLEAR'])
add('positive_false_interrupt',[e(0),e(1,False),e(2),e(3),e(4)],['PENDING','CLEAR','PENDING','PENDING','ACTIVE'])
add('unknown_before_open_breaks_dwell',[e(0),{'t':1,'c':'c1','p':'p1'},e(2),e(4)],['PENDING','UNKNOWN','PENDING','ACTIVE'],[False,False,False,True],['STATE','MISSING','STATE','STATE'])
add('unknown_active_retained_clock',[e(0),e(2),{'t':6,'c':'c1','p':'p1'},e(7)],['PENDING','ACTIVE','UNKNOWN','ESCALATED'],[False,True,True,True],['STATE','STATE','MISSING','STATE'])
add('unknown_breaks_clear_qualification',[e(0),e(2),e(3,False),e(4,None),e(5,False),e(6,False),e(7,False)],['PENDING','ACTIVE','ACTIVE','UNKNOWN','ACTIVE','ESCALATED','CLEAR'],[False,True,True,True,True,True,False],['STATE','STATE','STATE','CONFLICT','STATE','STATE','STATE'])
add('context_reset_dwell',[e(0),e(2),e(3,c='c2'),e(5,c='c2')],['PENDING','ACTIVE','PENDING','ACTIVE'],reasons=['STATE','STATE','CONTEXT_CHANGE','STATE'])
add('policy_reset_precedence',[e(0),e(2),e(3,c='c2',p='p2')],['PENDING','ACTIVE','PENDING'],reasons=['STATE','STATE','POLICY_CHANGE'])
add('reset_invalid_uses_quality_reason',[e(0),e(2),{'t':3,'c':'c2','p':'p2'}],['PENDING','ACTIVE','UNKNOWN'],[False,True,False],['STATE','STATE','MISSING'])
add('freshness_equality_valid',[e(2,o={'value':True,'c':'c1','p':'p1','at':0}),e(4,o={'value':True,'c':'c1','p':'p1','at':2})],['PENDING','ACTIVE'])
add('stale_then_fresh',[e(3,o={'value':True,'c':'c1','p':'p1','at':0}),e(4)],['UNKNOWN','PENDING'],[False,False],['STALE','STATE'])
add('future_evidence',[e(0,o={'value':True,'c':'c1','p':'p1','at':1})],['UNKNOWN'],[False],['FUTURE'])
add('context_mismatch_before_policy_age_conflict',[e(0,o={'value':None,'c':'wrong','p':'wrong','at':1})],['UNKNOWN'],[False],['CONTEXT_MISMATCH'])
add('policy_mismatch_before_age_conflict',[e(0,o={'value':None,'c':'c1','p':'wrong','at':1})],['UNKNOWN'],[False],['POLICY_MISMATCH'])
add('suppression_expiry_and_clock',[e(0),e(2,s={'c':'c1','p':'p1','until':6}),e(5,s={'c':'c1','p':'p1','until':6}),e(6,s={'c':'c1','p':'p1','until':6})],['PENDING','SUPPRESSED','SUPPRESSED','ESCALATED'])
add('stale_suppression_binding',[e(0),e(2,s={'c':'old','p':'p1','until':10}),e(3,s={'c':'c1','p':'old','until':10})],['PENDING','ACTIVE','ACTIVE'])
add('suppression_cannot_hide_unknown',[e(0),e(2),e(3,None,s={'c':'c1','p':'p1','until':10})],['PENDING','ACTIVE','UNKNOWN'],[False,True,True],['STATE','STATE','CONFLICT'])
add('milliseconds_normalize',[e(0),e(2000,unit='ms'),e(6000,unit='ms')],['PENDING','ACTIVE','ESCALATED'])
add('zero_durations',[e(0),e(1,False)],['ESCALATED','CLEAR'],policy={'D':0,'C':0,'E':0,'F':0})
add('observation_at_does_not_start_dwell',[e(2,o={'value':True,'c':'c1','p':'p1','at':0}),e(3)],['PENDING','PENDING'])
add('unchanged_false_control',[e(0,False),e(2,False),e(10,False)],['CLEAR','CLEAR','CLEAR'])
results=[]
for name,trace,policy,ref in cases:
    # Supply explicitly required seconds unit in intended valid historical cases.
    for event in trace: event.setdefault('unit','s')
    actual=oracle(trace,policy)
    results.append({'name':name,'trace':trace,'policy':policy,'expected':ref,'actual':actual,'pass':actual==ref})
invalid=[('duplicate_time',[e(0),e(0)],P),('decreasing_time',[e(1),e(0)],P),('bad_unit',[e(0,unit='minute')],P),('nonfinite_time',[e(float('nan'))],P),('integer_observation',[e(0,1)],P),('missing_context',[{'t':0,'p':'p1'}],P),('negative_duration',[e(0)],dict(P,D=-1)),('empty_observation',[e(0,o={})],P)]
for name,trace,policy in invalid:
    try:
        oracle(trace,policy); passed=False
    except ValueError:
        passed=True
    results.append({'name':name,'expected':'ValueError','pass':passed})
out={'author':'original expectations /root/alarm_semantics; post-evaluation v2 regression /root/final_review','basis':'Original independent expected transitions retained; three valid missing-observation packets corrected to include required unit=s before v2 regression. This is post-evaluation verification.','oracle_sha256':hashlib.sha256((base/'implementation/oracle_v2.py').read_bytes()).hexdigest(),'specification_sha256':hashlib.sha256((base/'protocol/SEMANTICS.md').read_bytes()).hexdigest(),'cases':results,'passed':sum(x['pass'] for x in results),'total':len(results)}
(base/'reviews/reference_checks_v2.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'passed':out['passed'],'total':out['total'],'failed':[x for x in results if not x['pass']]},indent=2))
assert out['passed']==out['total']
