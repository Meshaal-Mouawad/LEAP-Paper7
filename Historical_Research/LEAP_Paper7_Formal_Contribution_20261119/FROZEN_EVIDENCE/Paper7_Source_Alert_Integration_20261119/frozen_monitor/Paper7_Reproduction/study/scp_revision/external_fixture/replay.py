"""Projection of four Apache-2.0 Alertmanager TestSilencer expectations.
This runs Paper 7 only. It does not run Alertmanager.
"""
from pathlib import Path
import argparse,hashlib,json,sys,datetime,platform
HERE=Path(__file__).resolve().parent
STUDY=HERE.parent.parent

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(name,value): (HERE/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
def setup():
    lines=(HERE/'source/silence_test.go').read_text().splitlines()
    assertions=[(1383,False,'absent'),(1392,False,'nonmatching_exact'),(1402,True,'matching_exact'),(1408,False,'expired_exact')]
    unsupported=[(1419,False,'future_start','Scheduled start time is not represented by the native suppression contract.'),(1426,True,'scheduled_activation','Activation from a future StartsAt requires start-time semantics absent from the native contract.'),(1436,True,'additional_future_regex','Combines an existing active silence and another future regular-expression silence; multi-silence/start/regex semantics are outside the native contract.'),(1442,True,'overlapping_regex_activation','Overlapping silence expiration/activation and regular-expression matching are outside the native contract.')]
    def event(t):return dict(t=t,unit='s',c='bar',p='P0',o=dict(value=True,c='bar',p='P0',at=t))
    cases=[];ledger=[]
    for line,expected,name in assertions:
        token='require.True' if expected else 'require.False'
        assert token in lines[line-1] and 's.Mutes(model.LabelSet{"foo": "bar"})' in lines[line-1]
        q=3603 if name=='expired_exact' else 3
        trace=[event(0),event(2),event(q)]
        selected=None
        if name!='absent':
            selected='sil1' if name=='nonmatching_exact' else 'sil2'
            trace[-1]['s']=dict(c='baz' if selected=='sil1' else 'bar',p='P0',until=303)
        ident='Alertmanager_v0.28.1_TestSilencer_L'+str(line)
        cases.append(dict(id=ident,source_line=line,name=name,reference_mutes=expected,selected_source_silence=selected,trace=trace,policy=dict(D=2,C=2,E=4,F=2),base_severity='High'))
        ledger.append(dict(id=ident,line=line,name=name,expected_mutes=expected,status='mapped',source_assertion=lines[line-1].strip()))
    for line,expected,name,reason in unsupported:
        token='require.True' if expected else 'require.False'
        assert token in lines[line-1] and 's.Mutes' in lines[line-1]
        ledger.append(dict(id='Alertmanager_v0.28.1_TestSilencer_L'+str(line),line=line,name=name,expected_mutes=expected,status='outside_native_policy',reason=reason,source_assertion=lines[line-1].strip()))
    write('cases.json',cases)
    write('mapping.json',dict(source='prometheus/alertmanager@v0.28.1:silence/silence_test.go:TestSilencer',source_assertion_count=8,mapped_count=4,outside_native_policy_count=4,projection='foo exact label equality -> context equality; initial now -> t=3; fixed P0; suppress until now+300; query expiration at now+3600',ledger=ledger))
    paths=[HERE/'PROTOCOL.md',HERE/'replay.py',HERE/'mapping.json',HERE/'cases.json',*sorted((HERE/'source').iterdir()),STUDY/'implementation/monitor.py',STUDY/'implementation/oracle_v2.py']
    write('freeze.json',dict(frozen_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='frozen_before_replay',outputs_not_yet_created=not (HERE/'results.json').exists(),files=[dict(path=str(p.relative_to(STUDY)),sha256=sha(p)) for p in paths]))
    print('Frozen four mapped cases and all eight source assertions; no monitor execution.')

def replay():
    freeze=json.loads((HERE/'freeze.json').read_text())
    for x in freeze['files']:
        assert sha(STUDY/x['path'])==x['sha256'],'Frozen input changed: '+x['path']
    sys.path.insert(0,str(STUDY/'implementation'))
    from monitor import monitor
    from oracle_v2 import oracle
    cases=json.loads((HERE/'cases.json').read_text());rows=[]
    for c in cases:
        row=dict(id=c['id'],name=c['name'],source_line=c['source_line'],expected_mutes=c['reference_mutes'])
        try:
            observed=monitor(c['trace'],c['policy'],c['base_severity'])
            reference=oracle(c['trace'],c['policy'],c['base_severity'])
            actual=observed[-1]['state']=='SUPPRESSED'
            row.update(actual_mutes=actual,mapped_assertion_agreement=actual==c['reference_mutes'],active_before_query=observed[1]['active'],active_at_query=observed[-1]['active'],complete_oracle_agreement=observed==reference,monitor_output=observed,oracle_output=reference,execution_failure=None)
        except Exception as e:row.update(execution_failure=type(e).__name__+': '+str(e),mapped_assertion_agreement=False)
        rows.append(row)
    result=dict(run_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),python=sys.version,platform=platform.platform(),freeze_sha256=sha(HERE/'freeze.json'),alertmanager_executed=False,upstream_source_assertions=8,mapped_source_assertions=4,outside_native_policy=4,matched=sum(x['mapped_assertion_agreement'] for x in rows),execution_failures=sum(x['execution_failure'] is not None for x in rows),complete_oracle_agreement=all(x.get('complete_oracle_agreement',False) for x in rows),active_setup_verified=all(x.get('active_before_query',False) and x.get('active_at_query',False) for x in rows),cases=rows)
    write('results.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))
    assert result['matched']==4 and result['execution_failures']==0 and result['complete_oracle_agreement'] and result['active_setup_verified']
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['freeze','replay']);args=p.parse_args()
    setup() if args.mode=='freeze' else replay()
