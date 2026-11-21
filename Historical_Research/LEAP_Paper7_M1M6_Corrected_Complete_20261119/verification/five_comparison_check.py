"""Post-review test of five-comparison sufficiency on frozen Paper 7 traces.
This is a representation-only replay using the original monitor as decoder,
not a new independently designed monitor or new benchmark.
"""
from pathlib import Path
import sys, json, copy, hashlib
ROOT=Path(__file__).resolve().parents[1]
STUDY=ROOT/'replay/Paper7_Reproduction/saved_run'
sys.path.insert(0,str(STUDY/'implementation'))
from monitor import monitor

def canon(trace):
    out=[];previous=None
    curc=curp=0
    for e in trace:
        e2=copy.deepcopy(e)
        c,p=e['c'],e['p']
        if previous is not None:
            if c!=previous[0]:curc^=1
            if p!=previous[1]:curp^=1
        cv,pv='C'+str(curc),'P'+str(curp)
        e2['c'],e2['p']=cv,pv
        if 'o' in e:
            e2['o']['c']=cv if e['o']['c']==c else 'C_observation_mismatch'
            e2['o']['p']=pv if e['o']['p']==p else 'P_observation_mismatch'
        if 's' in e:
            joint=(e['s']['c']==c and e['s']['p']==p)
            e2['s']['c']=cv if joint else 'C_suppression_mismatch'
            e2['s']['p']=pv # no need to retain distinct suppression-mismatch reason
        out.append(e2)
        previous=(c,p)
    return out

def main():
    policy=json.loads((STUDY/'benchmark/policy.json').read_text())
    trials=events=0
    mismatches=[]
    all_reasons={}
    with (STUDY/'benchmark/traces.jsonl').open() as ins,(STUDY/'benchmark/reference.jsonl').open() as outs:
        for aline,bline in zip(ins,outs,strict=True):
            a,b=json.loads(aline),json.loads(bline)
            assert a['id']==b['id']
            new=monitor(canon(a['trace']),policy,a['severity'])
            expected=b['outputs']
            trials+=1;events+=len(expected)
            if new!=expected:
                mismatches.append(a['id'])
                if len(mismatches)>15:break
    result={'kind':'post-review five-comparison canonicalization replay',
        'status':'PASS' if not mismatches and trials==4935 and events==26430 else 'FAIL',
        'trace_count':trials,'event_count':events,'mismatched_complete_trace_or_reason':len(mismatches),'first_mismatches':mismatches,
        'frozen_trace_sha256':hashlib.sha256((STUDY/'benchmark/traces.jsonl').read_bytes()).hexdigest(),
        'reference_sha256':hashlib.sha256((STUDY/'benchmark/reference.jsonl').read_bytes()).hexdigest(),
        'interpretation':'Re-encoding checks sufficiency of version comparisons under the original monitor; does not establish an independent engine or minimum bit count.'}
    (ROOT/'reports/five_comparison_check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    assert result['status']=='PASS'
if __name__=='__main__': main()
