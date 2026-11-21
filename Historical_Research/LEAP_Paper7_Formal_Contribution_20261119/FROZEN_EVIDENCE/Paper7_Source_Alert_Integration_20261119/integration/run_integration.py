"""Offline source-to-alert integration; standard library; consumes preserved endpoints."""
import ast, csv, hashlib, importlib.util, itertools, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
HERE=Path(__file__).resolve().parent
OUT=HERE/'outputs'
OUT.mkdir(exist_ok=True)
EXP=ROOT/'recovered/LEAP_Paper7_Redesigned_Experiment_20261119/LEAP_Paper7_Redesigned_Experiment_20261119'
FROZEN=ROOT/'frozen_monitor/Paper7_Reproduction/saved_run'
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
mon=module('frozen_monitor',FROZEN/'implementation/monitor.py')
oracle=module('frozen_oracle',FROZEN/'implementation/oracle.py')
# Extract only functions: importing archived representation.py reruns its corpus.
representation_path=FROZEN/'r3/analysis/representation.py'
representation_tree=ast.parse(representation_path.read_text())
archived_three={}
exec(compile(ast.Module(body=[n for n in representation_tree.body if isinstance(n,ast.FunctionDef) and n.name in ['encode','decode']],type_ignores=[]),str(representation_path),'exec'),archived_three)
POLICY=json.loads((FROZEN/'benchmark/policy.json').read_text())
SCENARIOS=['fresh_positive','fresh_negative','old_observation','old_deferral','missing_observation','policy_change','old_policy_observation']
STRATEGIES=['A_file','B_calculation','C_documentation','D_dual']
KEYS=['state','active','severity']
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def writecsv(name,rows):
 with (OUT/name).open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def context(r,s,after):
 side='after' if after else 'before'
 c=r['structure_sha256_'+side];d=r['dossier_'+side+'_sha256']
 return {'A_file':r['file_sha256_'+side],'B_calculation':c,'C_documentation':d,'D_dual':canonical([c,d])}[s]
def trace(r,s,scenario):
 events=[]
 for t in [0,2,3,5,7,9]:
  after=t>=3;c=context(r,s,after);p='p1' if after and scenario in ['policy_change','old_policy_observation'] else 'p0'
  e=dict(t=t,unit='s',c=c,p=p)
  if not(after and scenario=='missing_observation'):
   e['o']=dict(at=t,value=not(after and scenario=='fresh_negative'),c=context(r,s,False) if after and scenario=='old_observation' else c,p='p0' if scenario=='old_policy_observation' else p)
  if scenario=='old_deferral':e['s']=dict(until=8,c=context(r,s,False),p='p0')
  events.append(e)
 return events

def encode(events,n):
 prev=None;out=[]
 for e in events:
  packet={k:e[k] for k in ['t','unit']};key=(e['c'],e['p'])
  dc=prev is not None and key[0]!=prev[0];dp=prev is not None and key[1]!=prev[1]
  if n==3:packet['reset']=dc or dp
  else:packet.update(context_changed=dc,policy_changed=dp)
  for channel,fields in [('o',['at','value']),('s',['until'])]:
   if channel not in e:continue
   z=e[channel];x={k:z[k] for k in fields};mc=z['c']==e['c'];mp=z['p']==e['p']
   if n==3 or (n==5 and channel=='s'):x['applies']=mc and mp
   else:x.update(context_matches=mc,policy_matches=mp)
   packet[channel]=x
  out.append(packet);prev=key
 return out

def decode(packets,n):
 ci=pi=False;out=[]
 for x in packets:
  if n==3:ci^=x['reset']
  else:ci^=x['context_changed'];pi^=x['policy_changed']
  c=str(ci);p=str(pi);e=dict(t=x['t'],unit=x['unit'],c=c,p=p)
  for channel in ['o','s']:
   if channel not in x:continue
   z=dict(x[channel])
   if 'applies' in z:mc=z.pop('applies');mp=True
   else:mc=z.pop('context_matches');mp=z.pop('policy_matches')
   z.update(c=c if mc else 'other',p=p if mp else 'other');e[channel]=z
  out.append(e)
 return out

def main():
 rows=list(csv.DictReader((EXP/'outputs/version_transition_events.csv').open()))
 rows=[r for r in rows if r['stratum']=='ARCHIVED_REVISION'];assert len(rows)==9
 details={x['case_id']:x for x in json.loads((EXP/'outputs/all_case_details.json').read_text())}
 allinputs=[];events=[];streams=[];changes=[];pairs=[];availability=[];representations=[]
 # Integration loops below execute each source-specific stream once; prior corpus untouched.
 for r in rows:
  for strategy in STRATEGIES:
   for scenario in SCENARIOS:
    ev=trace(r,strategy,scenario)
    assert encode(ev,3)==list(archived_three['encode'](ev))
    assert mon.monitor(decode(encode(ev,3),3),POLICY)==mon.monitor(archived_three['decode'](archived_three['encode'](ev)),POLICY)
 for r in rows:
  cid=r['case_id'];a=r['structure_changed']=='True';b=r['dossier_changed']=='True';ref=a or b
  pairs.append(dict(case_id=cid,calculation_representation_changed=a,documentation_changed=b,category=('both' if a and b else 'calculation_representation_only' if a else 'documentation_only' if b else 'neither'),runtime_status=details[cid]['runtime_status']))
  availability.append(dict(case_id=cid,observed_monitor_history_evaluable=False,reason='No recorded event timeline, Boolean finding, policy bindings or deferral history in supplied source-pair evidence',constructed_scenarios=7))
  for s in STRATEGIES:
   detected=context(r,s,False)!=context(r,s,True)
   changes.append(dict(case_id=cid,strategy=s,detected_change=detected,reference_dual_change=ref,false_reset=detected and not ref,missed_change=ref and not detected))
  for scenario in SCENARIOS:
   gold=oracle.oracle(trace(r,'D_dual',scenario),POLICY)
   for s in STRATEGIES:
    inp=trace(r,s,scenario);actual=mon.monitor(inp,POLICY);ownref=oracle.oracle(inp,POLICY)
    assert actual==ownref,(cid,s,scenario,'oracle mismatch')
    allinputs.append(dict(case_id=cid,strategy=s,scenario=scenario,provenance='OBSERVED_SOURCE_SIGNATURES_WITH_CONSTRUCTED_MONITORING_CONTEXT',events=inp))
    streams.append(dict(case_id=cid,strategy=s,scenario=scenario,state_differs_from_dual=any(x['state']!=y['state'] for x,y in zip(actual,gold)),severity_differs_from_dual=any(x['severity']!=y['severity'] for x,y in zip(actual,gold)),decision_differs_from_dual=any(any(x[k]!=y[k] for k in KEYS) for x,y in zip(actual,gold)),episode_differs_from_dual=any(x['active']!=y['active'] for x,y in zip(actual,gold)),reason_differs_from_dual=any(x['reason']!=y['reason'] for x,y in zip(actual,gold)),oracle_complete_agreement=actual==ownref))
    for i,(e,x,y) in enumerate(zip(inp,actual,gold)):
     events.append(dict(case_id=cid,strategy=s,scenario=scenario,event_index=i,t=e['t'],**x,reference_state=y['state'],reference_active=y['active'],reference_severity=y['severity'],reference_reason=y['reason']))
    for n in [3,5,6]:
     encoded=encode(inp,n);decoded=decode(encoded,n);result=mon.monitor(decoded,POLICY)
     agree=all(all(x[k]==y[k] for k in KEYS) for x,y in zip(actual,result));full=actual==result
     assert agree and (n==3 or full),(cid,s,scenario,n)
     representations.append(dict(case_id=cid,strategy=s,scenario=scenario,comparisons=n,decision_agreement=agree,complete_agreement=full,reason_event_differences=sum(x['reason']!=y['reason'] for x,y in zip(actual,result)),encoded_packets=encoded))
 # Positive checks against silent reason-loss and channel collapse.
 assert any(x['reason_event_differences'] for x in representations if x['comparisons']==3)
 assert sum(x['false_reset'] for x in changes if x['strategy']=='A_file')==2
 assert sum(x['missed_change'] for x in changes if x['strategy']=='B_calculation')==4
 assert sum(x['missed_change'] for x in changes if x['strategy']=='C_documentation')==1
 writecsv('pair_categories.csv',pairs);writecsv('change_detection.csv',changes);writecsv('decision_events.csv',events);writecsv('stream_comparisons.csv',streams);writecsv('actual_history_availability.csv',availability)
 writecsv('representation_results.csv',[{k:v for k,v in x.items() if k!='encoded_packets'} for x in representations])
 (OUT/'monitor_inputs.json').write_text(json.dumps(allinputs,indent=2)+'\n')
 (OUT/'comparison_packets.json').write_text(json.dumps(representations,indent=2)+'\n')
 summary=dict(real_source_pairs=9,source_transitions=4,constructed_contexts_per_pair=7,pair_contexts=63,strategies=4,strategy_streams=len(streams),events_per_stream=6,strategy_events=len(events),real_operational_histories_evaluable=dict(numerator=0,denominator=9),categories={c:sum(x['category']==c for x in pairs) for c in sorted({x['category'] for x in pairs})},technical_reference='dual representation revalidation, independent frozen oracle; chosen objective, not general correctness')
 summary['strategies']={s:dict(change_indicator_changes=dict(numerator=sum(x['detected_change'] for x in changes if x['strategy']==s),denominator=9),false_resets=dict(numerator=sum(x['false_reset'] for x in changes if x['strategy']==s),denominator=2),missed_changes=dict(numerator=sum(x['missed_change'] for x in changes if x['strategy']==s),denominator=7),**{k:dict(numerator=sum(x[k] for x in streams if x['strategy']==s),denominator=63) for k in ['state_differs_from_dual','severity_differs_from_dual','decision_differs_from_dual','episode_differs_from_dual','reason_differs_from_dual']}) for s in STRATEGIES}
 summary['representations']={str(n):dict(streams=sum(x['comparisons']==n for x in representations),decision_agreement=sum(x['decision_agreement'] for x in representations if x['comparisons']==n),complete_agreement=sum(x['complete_agreement'] for x in representations if x['comparisons']==n),reason_event_differences=sum(x['reason_event_differences'] for x in representations if x['comparisons']==n),event_denominator=1512) for n in [3,5,6]}
 summary['oracle_validation']=dict(complete_stream_agreement=252,denominator=252,checks='All unchanged monitor streams agree with frozen independent oracle. 3/5/6 assertions and explicit channel-error checks passed.')
 summary['per_field_event_differences']={s:{k:dict(numerator=sum(x[k]!=x['reference_'+k] for x in events if x['strategy']==s),denominator=378) for k in ['state','active','severity','reason']} for s in STRATEGIES}
 summary['all_strategies_identical_contexts']=[r['case_id']+'/'+scenario for r in rows for scenario in SCENARIOS if len({canonical([{k:x[k] for k in KEYS} for x in mon.monitor(trace(r,s,scenario),POLICY)]) for s in STRATEGIES})==1]
 summary['same_decision_cases']={s:[x['case_id']+'/'+x['scenario'] for x in streams if x['strategy']==s and not x['decision_differs_from_dual']] for s in STRATEGIES}
 summary['pairwise_strategy_decisions']={a+' vs '+b:dict(identical_streams=sum(all(all(x[k]==y[k] for k in KEYS) for x,y in zip(mon.monitor(trace(r,a,scenario),POLICY),mon.monitor(trace(r,b,scenario),POLICY))) for r in rows for scenario in SCENARIOS),denominator=63) for a,b in itertools.combinations(STRATEGIES,2)}
 report=['# Source-to-alert integration results','', 'Generated by run_integration.py. Nine real historical pairs across four Git transitions; seven constructed temporal contexts per pair. The 63 contexts are conditional probes, not 63 independent real cases. Actual recorded operational histories evaluable: 0/9.','', 'The calculation endpoint is a structural representation. Runtime status DIFFERENT does not necessarily mean a numerical output difference: P7R09 is a NameError-to-success change; P7R07 has unresolved input bindings; P7R01 has no runtime.','', 'Categories: '+', '.join(f'{k}={v}/9' for k,v in summary['categories'].items())+'.','', '| Strategy | Changed indicators | False resets / 2 reference-unchanged | Missed changes / 7 reference-changed | Decision differences / 63 | Episode differences / 63 | Reason differences / 63 | Identical decisions / 63 |','|---|---:|---:|---:|---:|---:|---:|---:|']
 for strategy,z in summary['strategies'].items():
  report.append('| '+strategy+' | '+str(z['change_indicator_changes']['numerator'])+'/9 | '+str(z['false_resets']['numerator'])+'/2 | '+str(z['missed_changes']['numerator'])+'/7 | '+str(z['decision_differs_from_dual']['numerator'])+'/63 | '+str(z['episode_differs_from_dual']['numerator'])+'/63 | '+str(z['reason_differs_from_dual']['numerator'])+'/63 | '+str(63-z['decision_differs_from_dual']['numerator'])+'/63 |')
 report+=['','Differences use the explicitly chosen dual-representation revalidation objective and frozen oracle, not a universal correctness assumption. All 252/252 streams match the oracle for their own inputs (1512/1512 event tuples).','', 'Three comparisons preserve decisions in 252/252 streams and 1512/1512 events. The specific joint decoder preserves reasons on 180/252 streams; 180/1512 event reasons differ. Five and six preserve all four fields on 252/252 streams and 1512/1512 events. The three-comparison implementation is checked against extracted archived encode/decode functions, without running the old corpus.','', 'Pairwise identical decision sequences:']
 report += [f'- {k}: {v["identical_streams"]}/{v["denominator"]}' for k,v in summary['pairwise_strategy_decisions'].items()]
 report+=['', 'Per-field event differences from dual reference (denominator 378 events per strategy):']
 report += [f'- {s}: '+', '.join(f'{k}={v["numerator"]}/{v["denominator"]}' for k,v in z.items()) for s,z in summary['per_field_event_differences'].items()]
 report+=['', 'Displayed-state and severity stream differences (denominator 63):']
 report += [f'- {s}: state={z["state_differs_from_dual"]["numerator"]}/63; severity={z["severity_differs_from_dual"]["numerator"]}/63' for s,z in summary['strategies'].items()]
 report+=['', 'All four strategies produce identical decision sequences in '+str(len(summary['all_strategies_identical_contexts']))+'/63 contexts: '+', '.join(summary['all_strategies_identical_contexts'])+'.', '', 'Reason examples at t=3: P7R06/fresh_positive gives CONTEXT_CHANGE under A versus STATE under D; P7R02/old_observation gives STATE under B versus CONTEXT_MISMATCH under D. In the constructed policy-change scenario, the joint decoder reports CONTEXT_CHANGE where the raw monitor reports POLICY_CHANGE. The old-policy-observation scenario similarly changes POLICY_MISMATCH to CONTEXT_MISMATCH; decision fields stay equal under three comparisons.']
 report += ['', 'Exact case/context identities with identical decisions are recorded in summary.json/same_decision_cases; all event fields and reference fields appear in decision_events.csv. All version-comparison inputs are in comparison_packets.json.','', 'The frozen 4935-trace benchmark, proofs, tables, figures, and source experiment outputs are consumed or preserved unchanged; they are not newly repeated here. The earlier 987/987 episode and 957/987 complete-decision agreement results concern the no_suppression_binding ablation; this integration does not replace those denominators.']
 (OUT/'RESULTS.md').write_text('\n'.join(report)+'\n')
 (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 consumed=[EXP/'outputs/version_transition_events.csv',EXP/'outputs/all_case_details.json',FROZEN/'implementation/monitor.py',FROZEN/'implementation/oracle.py',FROZEN/'benchmark/policy.json',representation_path,HERE/'PROTOCOL.md',Path(__file__)]
 (OUT/'consumed_manifest.json').write_text(json.dumps([dict(path=str(p.relative_to(ROOT)),sha256=digest(p)) for p in consumed],indent=2)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
