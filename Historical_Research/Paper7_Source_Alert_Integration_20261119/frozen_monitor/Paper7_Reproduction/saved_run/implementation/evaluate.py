"""Prespecified finite-trace analysis; writes raw decisions and exact counts."""
import pathlib,json,sys,collections,hashlib,time,platform,copy
from monitor import monitor,snapshot_baseline
ROOT=pathlib.Path(__file__).resolve().parents[1]
def sig(out):return [(x['state'],x['active'],x['severity']) for x in out]
def episodes(out):
 spans=[];start=None
 for i,x in enumerate(out):
  if x['active'] and start is None:start=i
  if not x['active'] and start is not None:spans.append((start,i));start=None
 if start is not None:spans.append((start,len(out)))
 return spans

def run(outdir='results'):
 dest=ROOT/outdir;dest.mkdir(exist_ok=True)
 freeze=json.loads((ROOT/'protocol/FREEZE.json').read_text())
 for name,h in freeze['sha256'].items():
  if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=h:raise RuntimeError('Freeze mismatch: '+name)
 refs={x['id']:x['outputs'] for x in map(json.loads,(ROOT/'benchmark/reference.jsonl').open())}
 policy=json.loads((ROOT/'benchmark/policy.json').read_text())
 methods=['bound','timer_only','no_evidence_binding','no_suppression_binding','no_freshness','snapshot']
 agg=collections.defaultdict(collections.Counter);outputs={};errors=[];t0=time.perf_counter()
 with (dest/'predictions.jsonl').open('w') as raw:
  for x in map(json.loads,(ROOT/'benchmark/traces.jsonl').open()):
   ref=refs[x['id']]
   for method in methods:
    try:o=snapshot_baseline(x['trace'],policy,x['severity']) if method=='snapshot' else monitor(x['trace'],policy,x['severity'],method)
    except Exception as ex:errors.append(dict(id=x['id'],method=method,error=repr(ex)));o=[]
    raw.write(json.dumps({'id':x['id'],'method':method,'outputs':o})+'\n')
    outputs[(x['id'],method)]=o
    keys=[(x['split'],method,'all'),(x['split'],method,x['mechanism']),(x['split'],method,'family:'+x['family'])]
    if x['variant']=='base':keys.append((x['split'],method,'base_only'))
    for key in keys:
     a=agg[key];a['traces']+=1;a['trace_agreement']+=sig(o)==sig(ref);a['episode_agreement']+=episodes(o)==episodes(ref);a['events']+=len(ref);a['failures']+=not bool(o)
     for p,r in zip(o,ref):
      a['event_agreement']+=(p['state'],p['active'],p['severity'])==(r['state'],r['active'],r['severity'])
      a['missed_active']+=r['active'] and not p['active'];a['unwarranted_active']+=p['active'] and not r['active'];a['reference_active']+=r['active'];a['reference_inactive']+=not r['active']
      a['severity_agreement']+=p['severity']==r['severity'];a['reason_agreement']+=p['reason']==r['reason'];a['unknown']+=p['state']=='UNKNOWN';a['reference_unknown']+=r['state']=='UNKNOWN'
 invariance=collections.defaultdict(collections.Counter)
 for (tid,method),o in outputs.items():
  group,variant=tid.rsplit('/',1)
  if variant!='base':
   invariance[method]['pairs']+=1;invariance[method]['equal']+=o==outputs[(group+'/base',method)]
 witnesses=json.loads((ROOT/'benchmark/witness_references.json').read_text());wa=[]
 for x in witnesses:
  field=x['projection_drop'];outer,inner=field.split('.')
  def project(trace):
   a=copy.deepcopy(trace)
   for e in a:
    if outer=='event':e.pop(inner,None)
    elif outer in e:e[outer].pop(inner,None)
   return a
  same=project(x['left'])==project(x['right']);different=sig(x['left_reference'])!=sig(x['right_reference'])
  wa.append(dict(id=x['id'],projection_identical=same,output_differs=different,first_different_event=next((i for i,(a,b) in enumerate(zip(sig(x['left_reference']),sig(x['right_reference']))) if a!=b),None),maximum_correct=1 if same and different else 2,total=2))
 summary={'metrics':[{'split':k[0],'method':k[1],'stratum':k[2],**dict(v)} for k,v in agg.items()], 'invariance':dict(invariance),'witnesses':wa,'errors':errors,'runtime_seconds':time.perf_counter()-t0,'environment':{'python':sys.version,'platform':platform.platform()},'freeze_sha256':hashlib.sha256((ROOT/'protocol/FREEZE.json').read_bytes()).hexdigest()}
 (dest/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps([x for x in summary['metrics'] if x['split']=='heldout' and x['stratum']=='all'],indent=2));print('Witnesses:',sum(x['projection_identical'] and x['output_differs'] for x in wa),'/',len(wa))
if __name__=='__main__':run(sys.argv[1] if len(sys.argv)>1 else 'results')
