"""Post-study verification only; no addition to frozen experiment denominators."""
from pathlib import Path
import sys,json,hashlib,time
from datetime import datetime,timezone
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'implementation'),str(ROOT/'replication_r2'),str(ROOT/'r3/baseline')]
from monitor import monitor
from oracle_v2 import oracle
from sqlite_baseline import sqlite_monitor
from pycontract_baseline import pycontract_monitor
methods={'Bound':monitor,'Reference_v2':oracle,'SQLite':sqlite_monitor,'PyContract':pycontract_monitor}
freeze=json.loads((OUT/'TARGETED_FREEZE.json').read_text())
for p,h in freeze['sha256'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
cases=json.loads((OUT/'targeted_cases.json').read_text());results=[];start=time.perf_counter()
for case in cases:
 outputs={};record={'id':case['id'],'expected_final':case['expected_final'],'methods':{}}
 for name,fn in methods.items():
  try:
   prediction=fn(case['trace'],case['policy'],'High');outputs[name]=prediction
   record['methods'][name]={'pass_final':prediction[-1]==case['expected_final'],'outputs':prediction,'error':None}
  except Exception as exc:record['methods'][name]={'pass_final':False,'outputs':None,'error':repr(exc)}
 record['all_full_sequences_equal']=len(outputs)==4 and all(v==outputs['Bound'] for v in outputs.values())
 record['pass']=record['all_full_sequences_equal'] and all(v['pass_final'] for v in record['methods'].values());results.append(record)
summary={'status':'post-evaluation targeted verification','utc':datetime.now(timezone.utc).isoformat(),'targeted_cases':len(results),'cases_passed':sum(r['pass'] for r in results),'method_case_checks':len(results)*4,'method_case_checks_passed':sum(v['pass_final'] for r in results for v in r['methods'].values()),'full_sequence_agreement_cases':sum(r['all_full_sequences_equal'] for r in results),'events_per_method':sum(len(c['trace']) for c in cases),'elapsed_seconds':time.perf_counter()-start,'source_hashes_verified':True}
(OUT/'targeted_results.json').write_text(json.dumps(results,indent=2));(OUT/'targeted_summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
assert all(r['pass'] for r in results)
