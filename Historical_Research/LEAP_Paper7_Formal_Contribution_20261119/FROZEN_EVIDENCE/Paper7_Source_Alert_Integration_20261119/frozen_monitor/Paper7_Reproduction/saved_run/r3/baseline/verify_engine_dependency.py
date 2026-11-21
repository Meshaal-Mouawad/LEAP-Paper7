"""Post-score integration check: verdicts require authentic engine dispatch."""
import sys,json
from pathlib import Path
sys.dont_write_bytecode=True
from pycontract_baseline import pycontract_monitor,pc
trace=[{'t':t,'unit':'s','c':'c1','p':'p1','o':{'value':True,'c':'c1','p':'p1','at':t}} for t in (0,2)]
p={'D':2,'C':2,'E':4,'F':2}
checks=[]
for owner,name,replacement in [(pc.Monitor,'eval',lambda self,e:None),(pc.Monitor,'eval_states',lambda self,e,s:None),(pc.State,'eval',lambda self,e:[self])]:
    original=getattr(owner,name)
    try:
        setattr(owner,name,replacement)
        try:pycontract_monitor(trace,p);observed='incorrectly succeeded'
        except RuntimeError as error:observed=str(error)
        checks.append({'disabled_engine_method':owner.__name__+'.'+name,'observed':observed,'pass':observed=='upstream dispatch count mismatch'})
    finally:setattr(owner,name,original)
restored,audit=pycontract_monitor(trace,p,audit=True)
assert [x['state'] for x in restored]==['PENDING','ACTIVE']
checks.append({'restored_engine':'actual unmodified upstream methods','audit':audit,'pass':True})
assert all(x['pass'] for x in checks)
Path(__file__).with_name('engine_dependency_checks.json').write_text(json.dumps(checks,indent=2))
print('4/4 engine dependency and restoration checks passed')
