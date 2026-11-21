"""Post-evaluation audit of already-frozen witnesses; generic class count."""
import json,copy,collections,pathlib,hashlib
from monitor import monitor
ROOT=pathlib.Path(__file__).resolve().parents[1]
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'))
def signature(x):return [(e['state'],e['active'],e['severity']) for e in x]
p=json.loads((ROOT/'benchmark/policy.json').read_text());w=json.loads((ROOT/'benchmark/witness_references.json').read_text());counts=collections.defaultdict(lambda:collections.defaultdict(collections.Counter));records=[]
for x in w:
 outer,inner=x['projection_drop'].split('.')
 for side in ['left','right']:
  ev=copy.deepcopy(x[side]);ref=x[side+'_reference'];full=monitor(ev,p)
  assert full==ref
  for e in ev:
   (e if outer=='event' else e.get(outer,{})).pop(inner,None)
  # Include every side input; benchmark IDs never enter monitor input.
  visible={'events':ev,'rule':x['rule'],'policy':p,'base_severity':'High'}
  key=canonical(visible);label=canonical(signature(ref));counts[x['projection_drop']][key][label]+=1
  records.append({'id':x['id']+'/'+side,'drop':x['projection_drop'],'projected_input':visible,'projection_sha256':hashlib.sha256(key.encode()).hexdigest(),'reference':ref})
summary=[]
for field,classes in counts.items():
 n=sum(sum(c.values()) for c in classes.values());b=sum(max(c.values()) for c in classes.values())
 summary.append(dict(field=field,N=n,classes=len(classes),heterogeneous_classes=sum(len(c)>1 for c in classes.values()),B=b,bound=b/n))
(ROOT/'results/information_classes.json').write_text(json.dumps(records,indent=2));(ROOT/'results/information_bound.json').write_text(json.dumps({'scope':'Audit of frozen witnesses; added after primary evaluation; no new performance inputs','summary':summary,'full_reference_agreement':len(records),'note':'Bounds are per projection. Six projections are separate interfaces, not one pooled accuracy population.'},indent=2));print(summary)
