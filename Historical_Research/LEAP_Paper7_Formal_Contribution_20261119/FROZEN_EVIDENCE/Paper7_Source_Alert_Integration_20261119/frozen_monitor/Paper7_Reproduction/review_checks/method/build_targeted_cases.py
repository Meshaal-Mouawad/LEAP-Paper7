"""Hand-calculated expected final decisions for concurrent policy conditions."""
from pathlib import Path
import json,copy
OUT=Path(__file__).resolve().parent
P={'D':2,'C':2,'E':4,'F':2}
def e(t,v=True,c='c1',p='p1',**kw):
 a={'t':t,'unit':'s','c':c,'p':p,'o':{'value':v,'c':c,'p':p,'at':t}};a.update(kw);return a
def sup(c='c1',p='p1',until=8):return {'c':c,'p':p,'until':until}
def obs(c='c1',p='p1',at=6,value=True):return dict(c=c,p=p,at=at,value=value)
C=[]
def add(name,last,state,active,severity,reason,extra=None,policy=None):
 trace=[e(0),e(2)]+(extra or [])+[last]
 C.append(dict(id=name,trace=trace,policy=policy or P,expected_final=dict(state=state,active=active,severity=severity,reason=reason)))
add('both_resets_valid_at_escalation',e(6,c='c2',p='p2'),'PENDING',False,'NONE','POLICY_CHANGE')
add('context_reset_valid_at_escalation',e(6,c='c2'),'PENDING',False,'NONE','CONTEXT_CHANGE')
add('both_resets_missing',{'t':6,'unit':'s','c':'c2','p':'p2'},'UNKNOWN',False,'UNKNOWN','MISSING')
add('both_resets_old_observation',e(6,c='c2',p='p2',o=obs()),'UNKNOWN',False,'UNKNOWN','CONTEXT_MISMATCH')
add('both_mismatches_future_conflict',e(6,o=obs(c='old',p='old',at=7,value=None)),'UNKNOWN',True,'UNKNOWN','CONTEXT_MISMATCH')
add('policy_mismatch_future_conflict',e(6,o=obs(p='old',at=7,value=None)),'UNKNOWN',True,'UNKNOWN','POLICY_MISMATCH')
add('future_conflict',e(6,o=obs(at=7,value=None)),'UNKNOWN',True,'UNKNOWN','FUTURE')
add('stale_conflict',e(6,o=obs(at=3,value=None)),'UNKNOWN',True,'UNKNOWN','STALE')
add('conflict_with_valid_suppression',e(6,None,s=sup()),'UNKNOWN',True,'UNKNOWN','CONFLICT')
add('missing_with_valid_suppression',{'t':6,'unit':'s','c':'c1','p':'p1','s':sup()},'UNKNOWN',True,'UNKNOWN','MISSING')
add('suppression_over_escalation',e(6,s=sup()),'SUPPRESSED',True,'NONE','SUPPRESSION')
add('suppression_expires_at_escalation',e(6,s=sup(until=6)),'ESCALATED',True,'HIGH','STATE')
add('clearing_completes_at_escalation',e(6,False),'CLEAR',False,'NONE','STATE',extra=[e(4,False)])
add('missing_when_clearing_would_complete',{'t':6,'unit':'s','c':'c1','p':'p1'},'UNKNOWN',True,'UNKNOWN','MISSING',extra=[e(4,False)])
add('both_resets_over_suppression_zero_dwell',e(6,c='c2',p='p2',s=sup(c='c2',p='p2')),'SUPPRESSED',True,'NONE','POLICY_CHANGE',policy=dict(P,D=0))
add('context_reset_over_suppression_zero_dwell',e(6,c='c2',s=sup(c='c2')),'SUPPRESSED',True,'NONE','CONTEXT_CHANGE',policy=dict(P,D=0))
add('stale_with_expired_suppression',e(6,o=obs(at=3),s=sup(until=6)),'UNKNOWN',True,'UNKNOWN','STALE')
add('both_resets_future',e(6,c='c2',p='p2',o=obs(c='c2',p='p2',at=7)),'UNKNOWN',False,'UNKNOWN','FUTURE')
add('both_resets_conflict',e(6,None,c='c2',p='p2'),'UNKNOWN',False,'UNKNOWN','CONFLICT')
add('context_reset_stale',e(6,c='c2',o=obs(c='c2',at=3)),'UNKNOWN',False,'UNKNOWN','STALE')
add('policy_reset_mismatch_stale',e(6,p='p2',o=obs(at=3)),'UNKNOWN',False,'UNKNOWN','POLICY_MISMATCH')
add('context_reset_invalid_suppression',e(6,c='c2',s=sup()),'PENDING',False,'NONE','CONTEXT_CHANGE')
add('negative_qualifying_suppressed_escalated',e(6,False,s=sup()),'SUPPRESSED',True,'NONE','SUPPRESSION')
add('clearing_completes_with_suppression',e(6,False,s=sup()),'CLEAR',False,'NONE','STATE',extra=[e(4,False)])
(OUT/'targeted_cases.json').write_text(json.dumps(C,indent=2))
print(len(C),'targeted traces with hand-calculated expected final decisions')
