from pathlib import Path
from collections import Counter,defaultdict
import hashlib,json,csv,copy
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
TYPES=['missing','conflict','stale','future','context_old_obs','policy_old_obs','context_fresh','policy_fresh','suppression_valid','suppression_old_context','suppression_old_policy'];POSITIONS=[2,3,5,7,9]
def event(t,v):return {'t':t,'unit':'s','c':'c1','p':'p1','o':{'value':v,'c':'c1','p':'p1','at':t}}
def expected(typ,j):
 a=[event(i,v) for i,v in enumerate([False]+[True]*7+[False]*4)]
 if typ=='missing':del a[j]['o']
 elif typ=='conflict':a[j]['o']['value']=None
 elif typ=='stale':a[j]['o']['at']=j-3
 elif typ=='future':a[j]['o']['at']=j+1
 elif typ in ['context_old_obs','context_fresh']:
  for e in a[j:]:e['c']='c2';e['o']['c']='c1' if typ=='context_old_obs' else 'c2'
 elif typ in ['policy_old_obs','policy_fresh']:
  for e in a[j:]:e['p']='p2';e['o']['p']='p1' if typ=='policy_old_obs' else 'p2'
 else:
  for e in a[j:]:e['s']={'c':'c0' if typ=='suppression_old_context' else 'c1','p':'p0' if typ=='suppression_old_policy' else 'p1','until':j+2}
 return a

def normalized(trace):
 a=[]
 for x in trace:
  scale=1 if x['unit']=='s' else .001;e={'t':x['t']*scale,'unit':'s','c':x['c'],'p':x['p']}
  if 'o' in x:e['o']={k:x['o'][k] for k in ['value','c','p','at']};e['o']['at']*=scale
  if 's' in x:e['s']={k:x['s'][k] for k in ['c','p','until']};e['s']['until']*=scale
  a.append(e)
 return a

def category(m):return 'four_symbol_sequences' if m=='exhaustive' else 'long_controls' if m=='control' else 'temporal_boundaries' if m.startswith('boundary_') else 'interventions'
def run():
 freeze=json.loads((ROOT/'protocol/FREEZE.json').read_text());hash_checks={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in freeze['sha256'].items()};assert all(hash_checks.values())
 rows=list(map(json.loads,(ROOT/'benchmark/traces.jsonl').read_text().splitlines()));refs={x['id']:x['outputs'] for x in map(json.loads,(ROOT/'benchmark/reference.jsonl').read_text().splitlines())}
 counts=defaultdict(lambda:dict(groups=set(),traces=0,events=0));grid=[];checks=[];reasons=defaultdict(Counter)
 for r in rows:
  m=r['mechanism'];k=(r['family'],r['split'],r['variant'],category(m),m);counts[k]['groups'].add(r['group']);counts[k]['traces']+=1;counts[k]['events']+=len(r['trace']);reasons[m].update(x['reason'] for x in refs[r['id']])
  if m in TYPES:
   j=int(r['group'].rsplit('/',1)[-1]);ok=normalized(r['trace'])==expected(m,j);checks.append({'id':r['id'],'type':m,'position':j,'pass':ok})
   if r['family']=='privacy' and r['variant']=='base':grid.append({'type':m,'position':j,'example_group':r['group'],'events':len(r['trace'])})
 assert len(checks)==825 and all(x['pass'] for x in checks)
 assert len(grid)==55 and {(x['type'],x['position']) for x in grid}=={(t,j) for t in TYPES for j in POSITIONS}
 table=[dict(zip(['family','split','variant','category','mechanism'],k),groups=len(v['groups']),traces=v['traces'],events=v['events']) for k,v in sorted(counts.items())]
 with (OUT/'taxonomy_full_counts.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(table[0]));w.writeheader();w.writerows(table)
 groups=defaultdict(set);traces=Counter();events=Counter()
 for r in rows:c=category(r['mechanism']);groups[c].add(r['group']);traces[c]+=1;events[c]+=len(r['trace'])
 summary={'original_hash_checks':hash_checks,'categories':{k:{'base_groups_all_families':len(groups[k]),'traces_all_families_variants':traces[k],'events_all_families_variants':events[k]} for k in groups},'total_groups':len({r['group'] for r in rows}),'total_traces':len(rows),'total_events':sum(len(r['trace']) for r in rows),'intervention_type_count':len(TYPES),'positions':POSITIONS,'intervention_pairs_per_family':len(grid),'intervention_records_checked':len(checks),'passed':sum(x['pass'] for x in checks),'reason_counts':{k:dict(v) for k,v in reasons.items()}}
 for name,obj in [('taxonomy_summary.json',summary),('intervention_grid_55.json',grid),('intervention_record_checks.json',checks)]: (OUT/name).write_text(json.dumps(obj,indent=2))
 print(json.dumps({k:v for k,v in summary.items() if k not in ['original_hash_checks','reason_counts']},indent=2))
if __name__=='__main__':run()
