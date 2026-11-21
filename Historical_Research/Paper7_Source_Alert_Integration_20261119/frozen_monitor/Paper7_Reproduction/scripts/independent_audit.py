"""Recalculate Paper 7 endpoints from saved inputs and raw outputs only.

Usage: python independent_audit.py RUN_DIRECTORY NEW_ANALYSIS_DIRECTORY
Uses no monitor, oracle, or original scoring helper imports.
"""
from pathlib import Path
import collections,csv,hashlib,json,sys

def rows(p): return [json.loads(s) for s in p.read_text().splitlines()]
def spans(outputs):
    active={i for i,o in enumerate(outputs) if o['active']}
    return sorted((i,next((j for j in range(i+1,len(outputs)+1) if j not in active),len(outputs)))
                  for i in active if i-1 not in active)
def decision(o): return (o['state'],o['active'],o['severity'])
def write_csv(path,data):
    with path.open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(data[0]));writer.writeheader();writer.writerows(data)
def main():
    root=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(exist_ok=False)
    traces=rows(root/'benchmark/traces.jsonl');refs=rows(root/'benchmark/reference.jsonl')
    byid={r['id']:r for r in traces};gold={r['id']:r['outputs'] for r in refs}
    assert len(byid)==len(traces)==len(gold)==len(refs)==4935
    assert set(byid)==set(gold)
    groups=collections.defaultdict(list);inventory=[];denom=collections.defaultdict(collections.Counter)
    for t in traces:
        tid=t['id'];ref=gold[tid];assert len(t['trace'])==len(ref)
        groups[t['group']].append(t)
        row={k:t[k] for k in ['id','group','source','family','rule','severity','split','mechanism','variant']}
        row.update(events=len(ref),reference_active=sum(o['active'] for o in ref),reference_inactive=sum(not o['active'] for o in ref),reference_unknown=sum(o['state']=='UNKNOWN' for o in ref),reference_episodes=len(spans(ref)))
        inventory.append(row)
        for stratum in ['all','variant:'+t['variant'],'family:'+t['family'],'mechanism:'+t['mechanism']]:
            c=denom[t['split'],stratum];c['traces']+=1
            for k in ['events','reference_active','reference_inactive','reference_unknown','reference_episodes']:c[k]+=row[k]
    assert len(groups)==1645
    for g,items in groups.items():
        assert len(items)==3 and {t['variant'] for t in items}=={'base','metadata','milliseconds'},g
        assert all(len({t[k] for t in items})==1 for k in ['split','source','family','mechanism']),g
    for k in ['source','family']:
        assert {t[k] for t in traces if t['split']=='development'}.isdisjoint({t[k] for t in traces if t['split']=='heldout'})
    write_csv(out/'design_inventory.csv',inventory)
    write_csv(out/'denominators.csv',[{'split':k[0],'stratum':k[1],**dict(v)} for k,v in sorted(denom.items())])
    methods={'bound','timer_only','no_evidence_binding','no_suppression_binding','no_freshness','snapshot'}
    raw=rows(root/'results/predictions.jsonl');pred={(r['id'],r['method']):r['outputs'] for r in raw}
    assert len(raw)==len(pred)==len(traces)*6
    assert set(pred)=={(t,m) for t in byid for m in methods}
    totals=collections.defaultdict(collections.Counter);base_mechanisms=collections.defaultdict(collections.Counter)
    for (tid,method),outputs in pred.items():
        t=byid[tid];ref=gold[tid];assert len(outputs)==len(ref),(tid,method)
        c=collections.Counter(traces=1,events=len(ref),failures=0,
            trace_agreement=int(list(map(decision,outputs))==list(map(decision,ref))),
            episode_agreement=int(spans(outputs)==spans(ref)))
        for p,r in zip(outputs,ref):
            c['event_agreement']+=decision(p)==decision(r)
            c['missed_active']+=r['active'] and not p['active']
            c['unwarranted_active']+=p['active'] and not r['active']
            c['reference_active']+=r['active'];c['reference_inactive']+=not r['active']
            c['severity_agreement']+=p['severity']==r['severity'];c['reason_agreement']+=p['reason']==r['reason']
            c['unknown']+=p['state']=='UNKNOWN';c['reference_unknown']+=r['state']=='UNKNOWN'
        strata=['all','family:'+t['family'],t['mechanism']]
        if t['variant']=='base':strata+=['base_only']
        for s in strata:totals[t['split'],method,s].update(c)
        if t['variant']=='base':base_mechanisms[t['split'],t['family'],t['mechanism'],method].update(c)
    historical=json.loads((root/'results/summary.json').read_text())
    assert not historical['errors']
    for row in historical['metrics']:
        key=(row['split'],row['method'],row['stratum'])
        assert dict(totals[key])=={k:v for k,v in row.items() if k not in ['split','method','stratum']},key
    write_csv(out/'endpoint_metrics.csv',[{'split':k[0],'method':k[1],'stratum':k[2],**dict(v)} for k,v in sorted(totals.items())])
    write_csv(out/'base_mechanism_metrics.csv',[{'split':k[0],'family':k[1],'mechanism':k[2],'method':k[3],**dict(v)} for k,v in sorted(base_mechanisms.items())])
    invariance={}
    for m in sorted(methods):
        equal=sum(pred[t['id'],m]==pred[t['group']+'/base',m] for t in traces if t['variant']!='base')
        invariance[m]={'pairs':3290,'equal':equal}
    assert invariance==historical['invariance']
    baseline={}
    for label,name in [('SQLite','replication_r2/predictions.jsonl'),('PyContract','r3/baseline/predictions.jsonl')]:
        data=rows(root/name);indexed={r['id']:r for r in data}
        assert len(data)==len(indexed)==len(byid) and set(indexed)==set(byid)
        assert all(r['error'] is None and r['outputs']==gold[r['id']] for r in data)
        if label=='PyContract':
            for r in data:
                n=len(gold[r['id']]);a=r['engine_audit'];assert a['engine_events']==a['state_transitions']==len(a['state_classes'])==n
        baseline[label]={'traces':len(data),'events':sum(len(r['outputs']) for r in data),'all_field_mismatches':0,'execution_errors':0}
    report={'independent_scoring':'No evaluator/monitor/oracle scoring helpers imported; raw JSONL rescored.',
        'total_traces':len(traces),'total_events':sum(len(t['trace']) for t in traces),'groups':len(groups),
        'split_and_variant_integrity':True,'all_original_metric_rows_equal':len(historical['metrics']),
        'heldout_all':dict(denom['heldout','all']),'heldout_base':dict(denom['heldout','variant:base']),
        'heldout_base_metrics':[{'method':m,**dict(totals['heldout',m,'base_only'])} for m in sorted(methods)],
        'metamorphic_invariance':invariance,'baseline_raw_output_checks':baseline,
        'input_hashes':{n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in ['benchmark/traces.jsonl','benchmark/reference.jsonl','results/predictions.jsonl','replication_r2/predictions.jsonl','r3/baseline/predictions.jsonl']}}
    (out/'INDEPENDENT_AUDIT.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__': main()
