"""Retrospective, separately frozen, matched-input SQLite replication."""
import json,sys,sqlite3,time,platform,hashlib,copy
from pathlib import Path
from collections import defaultdict
from datetime import datetime,timezone
sys.dont_write_bytecode=True
from sqlite_baseline import sqlite_monitor
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent

def blank():
    return dict(traces=0,trace_tuple_agreement=0,trace_all_fields_agreement=0,events=0,event_tuple_agreement=0,reason_agreement=0,severity_agreement=0,missed_active=0,unwarranted_active=0,reference_active=0,reference_inactive=0,episode_agreement=0,execution_failures=0)

def intervals(outputs):
    spans=[]; begin=None
    for i,o in enumerate(outputs):
        if o['active'] and begin is None: begin=i
        if not o['active'] and begin is not None: spans.append([begin,i]);begin=None
    if begin is not None: spans.append([begin,len(outputs)])
    return spans

def score(m,pred,ref):
    m['traces']+=1;m['events']+=len(ref)
    m['reference_active']+=sum(x['active'] for x in ref);m['reference_inactive']+=sum(not x['active'] for x in ref)
    if pred is None:
        m['execution_failures']+=1;return
    keys=('state','active','severity')
    eq=lambda a,b:tuple(a[k] for k in keys)==tuple(b[k] for k in keys)
    m['trace_tuple_agreement']+=len(pred)==len(ref) and all(eq(a,b) for a,b in zip(pred,ref))
    m['trace_all_fields_agreement']+=pred==ref
    m['episode_agreement']+=intervals(pred)==intervals(ref)
    for a,b in zip(pred,ref):
        m['event_tuple_agreement']+=eq(a,b)
        m['reason_agreement']+=a['reason']==b['reason']
        m['severity_agreement']+=a['severity']==b['severity']
        m['missed_active']+=b['active'] and not a['active']
        m['unwarranted_active']+=not b['active'] and a['active']

def malformed_cases():
    p={'D':2,'C':2,'E':4,'F':2}
    e={'t':0,'unit':'s','c':'c1','p':'p1','o':{'value':True,'c':'c1','p':'p1','at':0},'s':{'c':'c1','p':'p1','until':10}}
    cases=[]
    for key in ['t','unit','c','p']:
        a=copy.deepcopy(e);del a[key];cases.append(('missing_event_'+key,[a],p))
    for section,keys in [('o',['value','c','p','at']),('s',['c','p','until'])]:
        for key in keys:
            a=copy.deepcopy(e);del a[section][key];cases.append(('missing_'+section+'_'+key,[a],p))
    for key in p:
        pp=p.copy();del pp[key];cases.append(('missing_policy_'+key,[e],pp))
    for label,changes in [('invalid_unit',{'unit':'minutes'}),('nonfinite_time',{'t':float('inf')}),('bool_time',{'t':True}),('empty_context',{'c':''}),('empty_policy',{'p':''})]:
        a=copy.deepcopy(e);a.update(changes);cases.append((label,[a],p))
    for label,section,key,value in [('integer_value','o','value',1),('string_value','o','value','true'),('nonfinite_at','o','at',float('nan')),('nonfinite_until','s','until',float('inf'))]:
        a=copy.deepcopy(e);a[section][key]=value;cases.append((label,[a],p))
    cases.extend([('negative_duration',[e],dict(p,D=-1)),('nonfinite_duration',[e],dict(p,F=float('nan'))),('duplicate_time',[e,copy.deepcopy(e)],p),('decreasing_time',[dict(e,t=1),e],p)])
    return cases

def run():
    # Reject any change to frozen code/protocol/input/reference before execution.
    freeze=json.loads((HERE/'FREEZE_R2.json').read_text())
    for rel,digest in freeze['sha256'].items():
        if hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()!=digest:
            raise RuntimeError('freeze mismatch: '+rel)
    start=time.perf_counter();utc=datetime.now(timezone.utc).isoformat()
    policy=json.loads((ROOT/'benchmark/policy.json').read_text())
    references={x['id']:x['outputs'] for x in map(json.loads,(ROOT/'benchmark/reference.jsonl').read_text().splitlines())}
    metrics=defaultdict(blank); failures=[]
    with (HERE/'predictions.jsonl').open('w') as output:
        for rec in map(json.loads,(ROOT/'benchmark/traces.jsonl').read_text().splitlines()):
            error=None
            try: pred=sqlite_monitor(rec['trace'],policy,rec['severity'])
            except Exception as exc: pred=None;error=type(exc).__name__+': '+str(exc)
            ref=references[rec['id']]
            for key in ['overall','split/'+rec['split'],'family/'+rec['family'],'mechanism/'+rec['mechanism'],'variant/'+rec['variant']]:score(metrics[key],pred,ref)
            row={'id':rec['id'],'outputs':pred,'error':error,'equal_all_fields':pred==ref}
            output.write(json.dumps(row)+'\n')
            if pred!=ref:failures.append({'id':rec['id'],'error':error,'actual':pred,'reference':ref})
    witnesses=[]
    for rec in json.loads((ROOT/'benchmark/witness_references.json').read_text()):
        for side in ('left','right'):
            pred=sqlite_monitor(rec[side],policy,'High')
            ref=rec[side+'_reference']
            witnesses.append({'id':rec['id']+'/'+side,'outputs':pred,'reference':ref,'pass':pred==ref})
    hand=[]
    for rec in json.loads((ROOT/'reviews/reference_checks_v2.json').read_text())['cases']:
        if 'trace' not in rec:continue
        pred=sqlite_monitor(rec['trace'],rec['policy'],'High')
        hand.append({'name':rec['name'],'outputs':pred,'reference':rec['expected'],'pass':pred==rec['expected']})
    malformed=[]
    for name,trace,p in malformed_cases():
        try:sqlite_monitor(trace,p);result='accepted'
        except Exception as exc:result=type(exc).__name__
        malformed.append({'name':name,'expected':'ValueError','actual':result,'pass':result=='ValueError'})
    result={'replication':'R2 retrospective matched external-runtime baseline','utc_started':utc,'elapsed_seconds':time.perf_counter()-start,'runtime':{'python':sys.version,'sqlite':sqlite3.sqlite_version,'platform':platform.platform()},'frozen_inputs_verified':True,'metrics':dict(metrics),'witnesses':{'total':len(witnesses),'passed':sum(x['pass'] for x in witnesses)},'hand_traces':{'total':len(hand),'passed':sum(x['pass'] for x in hand)},'malformed_inputs':{'total':len(malformed),'passed':sum(x['pass'] for x in malformed)},'mismatching_trace_ids':[x['id'] for x in failures]}
    for name,obj in [('summary.json',result),('mismatches.json',failures),('witness_results.json',witnesses),('hand_trace_results.json',hand),('malformed_results.json',malformed)]:
        (HERE/name).write_text(json.dumps(obj,indent=2))
    print(json.dumps(result,indent=2))
if __name__=='__main__':run()
